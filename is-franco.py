import warnings
from asyncio import run
from LLM import ask_many
from utils import load_csv, save_csv


system_message = """
You will be given a movie title. If the movie title is in Arabic, respond with NO. If in Franco (Arabic written in English letters), respond with NO. Otherwise, respond with YES. These rules are very strict, never respond with anything else.

Examples:
- "أهلاً بالعيد" → "NO"
- "Fajia'a fok el haram" → "NO"
- "El bahr biyidhak lesh" → "NO"
- "Dans les rues d'Alexandrie" → "YES"
- "Home Cookin: Over 100 Years in the Making" → "YES"
"""


async def are_movies_in_franco(batch, load_path, save_path):
    movies = load_csv(load_path)

    tasks = await ask_many(
        system_message,
        [match["Title"] for match in movies[batch * 100 : (batch + 1) * 100]],
    )
    for i, task in enumerate(tasks):
        if task.strip().strip('"').lower() == "yes":
            continue
        elif task.strip().strip('"').lower() == "no":
            movies[batch * 100 + i]["Title"] = ""
        else:
            warnings.warn(
                f"Unexpected response from LLM: {task} for title: {movies[batch * 100 + i]['Title']}"
            )

    save_csv(save_path, movies, fieldnames=movies[0].keys())
    print("Corrected titles saved to ", save_path)


def main(config):
    batch = config["batch"]
    save_path = config["save_path"]
    load_path = config["load_path"]

    run(are_movies_in_franco(batch, load_path, save_path))
