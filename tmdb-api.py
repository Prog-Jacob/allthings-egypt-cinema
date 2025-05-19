import os
import time
import requests
from utils import save_csv
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
FIELDNAMES = ["tmdbID", "Title", "Year"]


def _tv_shows_url(action):
    return f"https://api.themoviedb.org/3/{action}/tv"


def _movies_url(action):
    return f"https://api.themoviedb.org/3/{action}/movie"


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


def main(args):
    action = args["action"]
    base_params = {
        "api_key": API_KEY,
        "include_adult": "true",
    }
    movies_params = {
        "url": _movies_url(action),
        "title_key": "title",
        "params": base_params,
        "year_key": "release_date",
    }
    tv_shows_params = {
        "url": _tv_shows_url(action),
        "title_key": "name",
        "params": base_params,
        "year_key": "first_air_date",
    }

    match action:
        case "search":
            movies_params["params"]["query"] = args["query"]
            tv_shows_params["params"]["query"] = args["query"]
        case "discover":
            movies_params["params"]["with_origin_country"] = "EG"
            tv_shows_params["params"]["with_origin_country"] = "EG"

    entries = []
    if args["exclude_movies"] is False:
        entries += fetch_entries(**movies_params)
    if args["exclude_tv_shows"] is False:
        entries += fetch_entries(**tv_shows_params)
    save_csv(args["save_path"], entries, FIELDNAMES)
