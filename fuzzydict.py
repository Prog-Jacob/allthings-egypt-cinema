from rapidfuzz import process
from Levenshtein import distance


class Dict(dict):
    def __init__(self, elements, threshold=5, is_fuzzy=True):
        super().__init__(elements)
        self.threshold = threshold
        self.is_fuzzy = is_fuzzy

    def get(self, key, default=None):
        if closest_key := self.closest_key(key):
            return self[closest_key]
        return default

    def closest_key(self, key):
        if not self.is_fuzzy:
            return key if key in self else None

        closest_key, closest_distance, _ = process.extractOne(
            key, self.keys(), scorer=distance
        )

        if closest_distance <= min(self.threshold, len(key) // 4):
            return closest_key

        return None
