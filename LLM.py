import asyncio
import aiohttp

# This script is under development.
# An LLM server must be up locally to run this script.
# I use LM Studio for this purpose, with qwen2.5.1-coder-7b-instruct model.


LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"


async def ask(session, system_message, user_message):
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {"role": "user", "content": user_message},
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


async def ask_many(system_message, user_messages):
    async with aiohttp.ClientSession() as session:
        tasks = [
            ask(session, system_message, user_message) for user_message in user_messages
        ]
        responses = await asyncio.gather(*tasks)
        return responses
