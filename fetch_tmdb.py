import os
import time
import requests
from utils import save_csv
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
FIELDNAMES = ["tmdbID", "Title", "Year"]
TV_SHOWS_URL = "https://api.themoviedb.org/3/discover/tv"
MOVIES_URL = "https://api.themoviedb.org/3/discover/movie"

params = {
    "api_key": API_KEY,
    "include_adult": "true",
    "with_origin_country": "EG",
}


def fetch_entries(url, title_key, year_key):
    page = 1
    movies = []
    params["sort_by"] = f"{year_key}.asc"

    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("results", [])

        for result in results:
            id = result.get("id")
            year = result.get(year_key, "")[:4]
            title = result.get(f"original_{title_key}", "") or result.get(title_key, "")
            movies.append(
                {
                    fieldname: value
                    for fieldname, value in zip(FIELDNAMES, [id, title, year])
                }
            )

        print(f"Fetched page {page}")
        time.sleep(0.1)
        if len(results) == 0:
            break
        page += 1

    return movies


if __name__ == "__main__":
    movies = fetch_entries(MOVIES_URL, "title", "release_date")
    tv_shows = fetch_entries(TV_SHOWS_URL, "name", "first_air_date")

    save_csv(f"./data/tmdb-mix-1to{len(movies)}.csv", movies, FIELDNAMES)
    save_csv(f"./data/tmdb-mix-1to{len(tv_shows) + 1}.csv", tv_shows, FIELDNAMES)
