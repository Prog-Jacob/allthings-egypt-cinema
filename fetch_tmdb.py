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
TV_SHOWS_SEARCH_URL = "https://api.themoviedb.org/3/search/tv"
MOVIES_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

base_params = {
    "api_key": API_KEY,
    "include_adult": "true",
}
movies_params = {
    "url": MOVIES_URL,
    "title_key": "title",
    "params": base_params,
    "year_key": "release_date",
}
tv_shows_params = {
    "url": TV_SHOWS_URL,
    "title_key": "name",
    "params": base_params,
    "year_key": "first_air_date",
}


def fetch_entries(url, title_key, year_key, params):
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
        time.sleep(0.02)
        if len(results) == 0:
            break
        page += 1

    return movies


def _process_call(fetch_params, save_path):
    entries = fetch_entries(**fetch_params)
    save_csv(save_path, entries, FIELDNAMES)


if __name__ == "__main__":
    movies_params["params"]["with_origin_country"] = "EG"
    tv_shows_params["params"]["with_origin_country"] = "EG"
    _process_call(movies_params, save_path="./data/tmdb-movies.csv")
    _process_call(tv_shows_params, save_path="./data/tmdb-movies.csv")
