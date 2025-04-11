from rapidfuzz import process
from Levenshtein import distance


class Dict(dict):
    def __init__(self, elements, threshold=5):
        super().__init__(elements)
        self.threshold = threshold

    def get(self, key, default=None):
        if key in self:
            return self[key]

        closest_key, closest_distance, _ = process.extractOne(
            key, self.keys(), scorer=distance
        )

        if closest_distance <= min(self.threshold, len(key) // 4):
            return self[closest_key]
        return default
