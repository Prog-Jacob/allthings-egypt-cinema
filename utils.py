import csv


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


def deduplicate_csv(filename, key=0):
    """Deduplicates a CSV file rows by a given key in place."""
    seen = set()
    deduplicated = []
    data = load_csv(filename)
    key = list(data[0].keys())[key] if isinstance(key, int) else key

    for item in data:
        if item[key] not in seen:
            seen.add(item[key])
            deduplicated.append(item)
    save_csv(filename, deduplicated, fieldnames=data[0].keys())


def numeric_column_csv(filename, key="Year", default=""):
    """Converts a CSV file column to integers in place."""
    data = load_csv(filename)
    for item in data:
        try:
            item[key] = int(item[key])
        except ValueError:
            item[key] = default
    save_csv(filename, data, fieldnames=data[0].keys())


def take_columns_csv(filename, columns):
    """Takes only the specified columns from a CSV file in a new file."""
    data = load_csv(filename)
    data = [{key: item[key] for key in columns} for item in data]
    save_csv(f"{filename}-{'-'.join(columns)}.csv", data, fieldnames=columns)
