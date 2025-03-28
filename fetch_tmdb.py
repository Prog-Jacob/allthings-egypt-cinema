import os
import csv
import time
import requests
from dotenv import load_dotenv


load_dotenv()

START = 1
END = 250
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/discover/movie"

params = {
    "page": START,
    "api_key": API_KEY,
    "with_origin_country": "EG",
    "sort_by": "release_date.asc",
}

movies = []

for page in range(START, END):
    params["page"] = page
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    for movie in data.get("results", []):
        id = movie.get("id")
        year = movie.get("release_date", "")[:4]
        title = movie.get("original_title", "") or movie.get("title", "")
        movies.append([id, title, year])

    print(f"Fetched page {page}")
    time.sleep(0.2)


with open(
    f"tmdb_egypt_movies_{START}_{END}.csv", "w", newline="", encoding="utf-8"
) as f:
    writer = csv.writer(f)
    writer.writerow(["tmdbID", "Title", "Year"])
    writer.writerows(movies)
