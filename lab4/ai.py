import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.hits = set()

    def record_result(self, pos, hit):
        if hit:
            self.hits.add(pos)

    def choose(self):
        options = [(r, c) for r in range(self.size) for c in range(self.size)
                   if (r, c) not in self.tried]
        if not options:
            return None

        adjacent = [
            (row + row_offset, column + column_offset)
            for row, column in self.hits
            for row_offset, column_offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if 0 <= row + row_offset < self.size
            and 0 <= column + column_offset < self.size
            and (row + row_offset, column + column_offset) not in self.tried
        ]
        candidates = adjacent or options
        pos = random.choice(candidates)
        self.tried.add(pos)
        return pos
