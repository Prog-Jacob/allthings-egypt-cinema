#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/assets"
TEMP_DIR="$SCRIPT_DIR/temp"
README="$SCRIPT_DIR/README.md"
VERSION="v$(date +%Y.%m.%d)"

mkdir -p "$TEMP_DIR"

find_asset() {
    local files=("$ASSETS_DIR"/$1)
    [[ -e "${files[0]}" ]] && echo "${files[0]}"
}

count_lines() {
    tail -n +2 "$1" 2>/dev/null | wc -l | tr -d ' '
}

extract_count() {
    echo "$1" | grep -oE '[0-9]+\.csv$' | grep -oE '[0-9]+'
}

process_source() {
    local name="$1"
    local pattern="$2"
    local fetch_cmd="$3"
    local key="$4"

    local asset
    asset="$(find_asset "${pattern}-1to*.csv")" || true
    [[ -z "$asset" ]] && return

    local fresh_file="$TEMP_DIR/${name}-fresh.csv"

    echo "[$name] Current: $(basename "$asset")"

    # Fetch fresh data
    eval "$fetch_cmd"

    # Cross-check for new entries
    python "$SCRIPT_DIR/run.py" cross-check \
        --first-path "$asset" \
        --second-path "$fresh_file" \
        --first-key "$key" \
        --second-key "$key" \
        --join-type right-outer \
        --is-fuzzy False \
        --save-path "$TEMP_DIR/new-$name"

    # Replace asset only if fresh data has more entries
    local old_count
    local fresh_count
    old_count="$(extract_count "$asset")"
    fresh_count="$(count_lines "$fresh_file")"

    if [[ "$fresh_count" -gt "$old_count" ]]; then
        local new_asset="$ASSETS_DIR/${pattern}-1to${fresh_count}.csv"

        mv "$fresh_file" "$new_asset"
        rm "$asset"

        echo "[$name] Updated: $(basename "$new_asset") (+$((fresh_count - old_count)))"
    else
        rm "$fresh_file"
        echo "[$name] No new entries"
    fi
}

# TMDb Movies
process_source \
    "tmdb-movies" \
    "tmdb-mix-movies" \
    "python '$SCRIPT_DIR/run.py' tmdb-api discover \
        --exclude-tv-shows True \
        --save-path '$TEMP_DIR/tmdb-movies-fresh.csv'" \
    "tmdbID"

# TMDb TV Shows
process_source \
    "tmdb-tvshows" \
    "tmdb-mix-tvshows" \
    "python '$SCRIPT_DIR/run.py' tmdb-api discover \
        --exclude-movies True \
        --save-path '$TEMP_DIR/tmdb-tvshows-fresh.csv'" \
    "tmdbID"

# Letterboxd
process_source \
    "letterboxd" \
    "letterboxd-mix" \
    "(cd '$SCRIPT_DIR/scrapers' && npm run run:letterbox --silent) && \
        mv '$SCRIPT_DIR/scrapers/letterboxd_movies.csv' '$TEMP_DIR/letterboxd-fresh.csv'" \
    "url"

# Update README
update_readme() {
    local pattern="$1"
    local asset
    asset="$(find_asset "${pattern}-1to*.csv")" || true
    [[ -z "$asset" ]] && return

    local count
    count="$(extract_count "$asset")"
    sed -i '' -E "s/${pattern}-1to[0-9]+\.csv/${pattern}-1to${count}.csv/g" "$README"
}

sed -i '' -E "s/v[0-9]{4}\.[0-9]{2}\.[0-9]{2}/${VERSION}/g" "$README"
update_readme "tmdb-mix-movies"
update_readme "tmdb-mix-tvshows"
update_readme "letterboxd-mix"

echo "[readme] Updated to $VERSION"
echo "Done. Temp files in: $TEMP_DIR"
