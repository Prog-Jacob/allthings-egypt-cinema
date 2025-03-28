import asyncio
import aiohttp
from cross_check import load_csv, save_csv

# This script is under development.
# An LLM server must be up locally to run this script.
# I use LM Studio for this purpose, with qwen2.5.1-coder-7b-instruct model.


LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"


async def fetch_fixed_titles(session, movie):
    messages = [
        {
            "role": "system",
            "content": """
You will be given a movie title. If the movie title is in Arabic, respond with the movie title. If in Franco (Arabic written in English letters), respond with the original Arabic title. If in English or there's any issue, respond with empty string.

Examples:
- "أهلاً بالعيد" → "اهلاً بالعيد"
- "Fajia'a fok el haram" → "فاجعة فوق الهرم"
- "El bahr biyidhak lesh" → "البحر بيضحك ليش"
- "Home Cookin: Over 100 Years in the Making" → ""
""",
        },
        {"role": "user", "content": movie["Title"]},
    ]
    payload = {
        "model": "qwen2.5.1-coder-7b-instruct",
        "messages": messages,
        "temperature": 0.7,
        "stream": False,
    }

    async with session.post(LLM_URL, json=payload) as response:
        result = await response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")


async def process_titles(matches):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_fixed_titles(session, match) for match in matches]
        responses = await asyncio.gather(*tasks)

        for j, title in enumerate(responses):
            matches[j]["Title"] = title.strip().strip('"')


def main():
    batch = int(input("Enter batch number: "))
    matches = load_csv("matches_corrected.csv")

    asyncio.run(process_titles(matches[batch * 100 : (batch + 1) * 100]))

    save_csv("matches_corrected.csv", matches, fieldnames=matches[0].keys())
    print("Corrected titles saved to matches_corrected.csv")


if __name__ == "__main__":
    main()
