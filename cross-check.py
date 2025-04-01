from fuzzydict import Dict
from utils import load_csv, save_csv


def cross_check(host_list, dest_list):
    host_set = Dict(
        {
            item["Name"].strip().lower(): item["Year"].strip().lower()
            for item in host_list
        }
    )
    dest_set = {item["Title"].strip().lower(): item for item in dest_list}

    dest_list = [
        (item["Title"].strip().lower(), int(item["Year"].strip().lower() or "0"))
        for item in dest_list
    ]
    matches = [
        item[0]
        for item in dest_list
        if abs(int(host_set.get(item[0], "100000") or item[1]) - item[1]) > 4
    ]

    return [dest_set[item] for item in matches]


def main(config):
    host_path = config["host_path"]
    dest_path = config["dest_path"]
    save_path = config["save_path"]

    host_list = load_csv(host_path)
    dest_list = load_csv(dest_path)

    matches = cross_check(host_list, dest_list)
    print(f"Found {len(matches)} matches:")

    save_csv(save_path, matches, fieldnames=matches[0].keys())
    print("Matches saved to ", save_path)
