from Levenshtein import distance


class Dict(dict):
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
