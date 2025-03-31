from asyncio import run
from LLM import ask_many
from config import get_config
from utils import load_csv, save_csv


system_message = """
You will be given a movie title. If the movie title is in Arabic, respond with the movie title. If in Franco (Arabic written in English letters), respond with the original Arabic title. If in English or there's any issue, respond with empty string.

Examples:
- "أهلاً بالعيد" → "اهلاً بالعيد"
- "Fajia'a fok el haram" → "فاجعة فوق الهرم"
- "El bahr biyidhak lesh" → "البحر بيضحك ليش"
- "Home Cookin: Over 100 Years in the Making" → ""
"""


async def convert_movies_from_franco(batch, load_path, save_path):
    movies = load_csv(load_path)

    tasks = await ask_many(
        system_message,
        [match["Title"] for match in movies[batch * 100 : (batch + 1) * 100]],
    )
    for i, task in enumerate(tasks):
        movies[batch * 100 + i]["Title"] = task

    save_csv(save_path, movies, fieldnames=movies[0].keys())
    print("Corrected titles saved to ", save_path)


if __name__ == "__main__":
    config = get_config("llm")
    batch = config["batch"]
    save_path = config["save_path"]
    load_path = config["load_path"]

    run(convert_movies_from_franco(batch, load_path, save_path))
