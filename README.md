# Allthings Egypt

The [**Allthings Egypt**](https://letterboxd.com/prog_jacob/list/allthings-egypt/) list gathers <b>Egyptian films</b> as well as <b>international productions</b> that feature Egypt as a setting, subject, or part of the narrative. It is organized <em>chronologically by <b>release date</b></em>, from the oldest to the newest, to provide a sense of how Egypt’s representation in cinema has evolved over time.

## &#128680; Help Needed: 1,000 More Films to Add! &#128680;

There is an additional <b>list of 4,500 movies</b>, which I estimate contains around <b>1,000 films not yet included here</b>. However, there's <b>no reliable way to import them</b> because they lack their <b>original titles</b>. To fix this, I need help verifying and retrieving these missing titles. Anyone can <b>anonymously contribute</b> by adding a movie or two to this 👉 <a href="https://docs.google.com/spreadsheets/d/1UD2LSrXbXFD8ttaELjEe_JtkTwyVUyZm1sadbZDgoRA/edit?usp=sharing"><b>Google Sheet</b></a> 👈.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Letterboxd](https://img.shields.io/badge/Letterboxd-5,407%20Movies-movie?logo=letterboxd&logoColor=fff&style=flat)](https://letterboxd.com/prog_jacob/list/allthings-egypt/)

## About this Project

This repository contains the scripts and data used to compile the [**Allthings Egypt**](https://letterboxd.com/prog_jacob/list/allthings-egypt/) movie list, which aims to be the most comprehensive collection of films related to Egypt. The scripts are not part of a structured project but rather a collection of useful tools for gathering, processing, and cross-referencing movie data from different sources such as IMDb, TMDb, and Letterboxd.

## Data Files

This repository includes several datasets, each representing movie lists from different sources:

- [**`letterboxd_url_1to4746`**](./data/letterboxd-url-1to4746.csv) – A list of [**Letterboxd**](https://letterboxd.com/films/country/egypt/) movie URLs.
- [**`imdb_mix_1to6396`**](./data/imdb-mix-1to6396.csv) – A collection of movies scraped from [**IMDb**](https://www.imdb.com/search/title/?title_type=feature,tv_series,short,tv_miniseries,tv_movie,tv_special,tv_short,video&countries=EG&sort=release_date,asc).
- [**`tmdb_mix_1to4258`**](./data/tmdb-mix-1to4258.csv) – A dataset containing movie entries from [**TMDb**](https://developer.themoviedb.org/reference/discover-movie).
- [**`allthings-egypt`**](./data/allthings-egypt.csv) – The primary dataset compiling all relevant films related to Egypt.

## Available Scripts

### Data Collection

- **`fetch_tmdb.py`** – Fetches movie data from the TMDb API, retrieving pages from a specified `START` to `END` range pages. Requires an API key set in a `.env` file as `TMDB_API_KEY=Your-Free-Api-Key-Here`.

- **`scrapers/imdb.js`** – Contains functions meant to run in the browser console of IMDb pages. These include:

  - `clickLoadMore(N)`: Clicks the "Load More" button `N` times.
  - Code blocks to parse movie data and copy the resulting CSV rows to the clipboard.

- **`scrapers/letterboxd.js`** – Provides a similar tool for extracting movie data from Letterboxd. Currently, scraping must be done page by page manually.

### Data Processing

- **`cross_check.py`** – Compares a **destination list** (CSV file) with a **host list** to identify missing movies.
- **`utils.py`** – A set of helper functions for CSV manipulation, including `loading` and `saving` files, `deduplicating` rows given a reference column, and `extracting` columns to a new CSV file.

### Additional Utilities

- **`fuzzydict.py`** – A custom dictionary class that extends Python’s `dict`. The `get()` method returns the closest matching key based on edit distance, useful for handling inconsistencies in movie titles.
- **`convert_franco.py`** - A work in progress as an attempt to convert the **Franco** titles to their original titles using an LLM.

## License

This repository is licensed under the [MIT License](LICENSE). Feel free to use and modify the scripts as needed.

---

For questions or contributions, feel free to open an issue, submit a pull request, or [contact me](mailto:ahmed.abdelaziz.gm@gmail.com)!
