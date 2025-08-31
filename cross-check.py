from fuzzydict import Dict
from utils import load_csv, save_csv


def numerize_string(text):
    return int(text.strip().lower() or "0")


def cross_check(
    first_list,
    second_list,
    first_key,
    second_key,
    joining_type="inner-left",
    is_fuzzy=False,
):
    first_set = {item[first_key].strip().lower(): item for item in first_list}
    second_set = {item[second_key].strip().lower(): item for item in second_list}

    lookup_dict = Dict(first_set, is_fuzzy=is_fuzzy)

    matches = [
        (lookup_dict.closest_key(key), key)
        for key, item in second_set.items()
        if lookup_dict.get(key) is not None
        and (
            not is_fuzzy
            or numerize_string(item.get("Year", "0")) == 0
            or numerize_string(lookup_dict.get(key).get("Year", "0")) == 0
            or abs(
                numerize_string(item.get("Year", "0"))
                - numerize_string(lookup_dict.get(key).get("Year", "0"))
            )
            <= 4
        )
    ]
    first_matches = [key for (key, _) in matches]
    second_matches = [key for (_, key) in matches]

    match joining_type:
        case "inner-left":
            return [[first_set[key] for key in first_matches]]
        case "inner-right":
            return [[second_set[key] for key in second_matches]]
        case "outer":
            return [
                [item for key, item in first_set.items() if key not in first_matches],
                [item for key, item in second_set.items() if key not in second_matches],
            ]
        case "left-outer":
            return [
                [item for key, item in first_set.items() if key not in first_matches]
            ]
        case "right-outer":
            return [
                [item for key, item in second_set.items() if key not in second_matches]
            ]
        case _:
            return []


def main(config):
    first_path = config["first_path"]
    second_path = config["second_path"]
    first_key = config["first_key"]
    second_key = config["second_key"]
    save_path = config["save_path"]
    join_type = config["join_type"]
    is_fuzzy = config["is_fuzzy"]

    first_list = load_csv(first_path)
    second_list = load_csv(second_path)

    matches = cross_check(
        first_list, second_list, first_key, second_key, join_type, is_fuzzy
    )

    for i, match in enumerate(matches):
        if len(match) == 0:
            continue
        path = f"{save_path}_{i}.csv"
        save_csv(path, match, fieldnames=match[0].keys())
        print(f"Saved {len(match)} matches to {path}")
