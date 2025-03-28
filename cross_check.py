import csv
from Levenshtein import distance


class FuzzyDict(dict):
    def __init__(self, elements, threshold=5):
        super().__init__(elements)
        self.threshold = threshold
        self.map = dict(elements)

    def get(self, key, default=None):
        if key in self.map:
            return self.map[key]
        threshold = 1000000
        best_match = None

        for item_title, item_year in self.items():
            dist = distance(item_title, key)
            if dist < threshold:
                threshold = dist
                best_match = item_year

        if threshold <= min(self.threshold, len(key) // 4):
            return best_match
        return default


def save_csv(filename, data, fieldnames):
    """Saves a list of dictionaries to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def load_csv(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def cross_check(list1, list2):
    set1 = FuzzyDict(
        {item["Name"].strip().lower(): item["Year"].strip().lower() for item in list1}
    )
    set2 = {item["Title"].strip().lower(): item for item in list2}

    matches = [
        (item["Title"].strip().lower(), item["Year"].strip().lower()) for item in list2
    ]
    matches = [item for item in matches if item[1]]
    matches = [(item[0], int(item[1])) for item in matches]

    matches = [item for item in matches if set1.get(item[0], True)]
    matches = [
        item for item in matches if abs(int(set1.get(item[0], "0")) - item[1]) > 4
    ]

    return [set2[item[0]] for item in matches]


def main():
    first_list = load_csv(
        "allthings-egypt.csv"
    )  # Position,Name,Year,URL,Description  ->   Downloaded from Letterboxd
    second_list = load_csv(
        "data_imdb_mix_1_6336.csv"
    )  # imdbID,Title,Year  ->   Scraped with ./scrapers/imdb.js

    matches = cross_check(first_list, second_list)

    print(f"Found {len(matches)} matches:")
    save_csv("matches.csv", matches, fieldnames=matches[0].keys())
    print("Matches saved to matches.csv")


if __name__ == "__main__":
    main()
