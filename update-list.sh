#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/assets"
TEMP_DIR="$SCRIPT_DIR/temp"

mkdir -p "$TEMP_DIR"

find_asset() {
    local files=("$ASSETS_DIR"/$1)
    [[ -e "${files[0]}" ]] && echo "${files[0]}"
}

count_lines() {
    tail -n +2 "$1" 2>/dev/null | wc -l | tr -d ' '
}

update_asset() {
    local name="$1"
    local asset="$2"
    local fresh="$3"
    local key="$4"

    echo "[$name] Current: $(basename "$asset")"

    python "$SCRIPT_DIR/run.py" cross-check \
        --first-path "$asset" \
        --second-path "$fresh" \
        --first-key "$key" \
        --second-key "$key" \
        --join-type right-outer \
        --is-fuzzy False \
        --save-path "$TEMP_DIR/new-$name"

    echo "[$name] Cross-check saved: new-${name}_0.csv"

    local fresh_count
    fresh_count="$(count_lines "$fresh")"

    local new_asset="${asset%%-1to*}-1to${fresh_count}.csv"

    mv "$fresh" "$new_asset"
    rm "$asset"

    echo "[$name] Replaced with $fresh_count entries -> $(basename "$new_asset")"
}

# TMDb Movies
if asset="$(find_asset "tmdb-mix-movies-1to*.csv")"; [[ -n "$asset" ]]; then
    python "$SCRIPT_DIR/run.py" tmdb-api discover \
        --exclude-tv-shows True \
        --save-path "$TEMP_DIR/tmdb-movies-fresh.csv"

    update_asset \
        "tmdb-movies" \
        "$asset" \
        "$TEMP_DIR/tmdb-movies-fresh.csv" \
        "tmdbID"
fi

# TMDb TV Shows
if asset="$(find_asset "tmdb-mix-tvshows-1to*.csv")"; [[ -n "$asset" ]]; then
    python "$SCRIPT_DIR/run.py" tmdb-api discover \
        --exclude-movies True \
        --save-path "$TEMP_DIR/tmdb-tvshows-fresh.csv"

    update_asset \
        "tmdb-tvshows" \
        "$asset" \
        "$TEMP_DIR/tmdb-tvshows-fresh.csv" \
        "tmdbID"
fi

# Letterboxd
if asset="$(find_asset "letterboxd-mix-1to*.csv")"; [[ -n "$asset" ]]; then
    (
        cd "$SCRIPT_DIR/scrapers"
        npm run run:letterbox --silent
    )

    mv "$SCRIPT_DIR/scrapers/letterboxd_movies.csv" \
       "$TEMP_DIR/letterboxd-fresh.csv"

    update_asset \
        "letterboxd" \
        "$asset" \
        "$TEMP_DIR/letterboxd-fresh.csv" \
        "url"
fi

echo "Done. Temp files in: $TEMP_DIR"
