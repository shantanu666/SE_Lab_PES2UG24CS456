class Board:
    SIZE = 6

    def __init__(self):
        self.ships = set()
        self.fleet = []
        self.ship_hits = []
        self.shots = set()
        self.shot_results = {}

    def place_ship(self, cells):
        ship = set(cells)
        if not ship:
            raise ValueError("A ship must occupy at least one cell.")
        if self.ships.intersection(ship):
            raise ValueError("Ships cannot overlap.")
        self.ships.update(ship)
        self.fleet.append(ship)
        self.ship_hits.append(set())

    def fire(self, pos):
        if pos in self.shots:
            raise ValueError("Already fired at this coordinate.")
        self.shots.add(pos)
        for ship, hits in zip(self.fleet, self.ship_hits):
            if pos in ship:
                hits.add(pos)
                self.shot_results[pos] = True
                return True
        self.shot_results[pos] = False
        return False

    @property
    def sunk_ships(self):
        return {
            frozenset(ship)
            for ship, hits in zip(self.fleet, self.ship_hits)
            if ship <= hits
        }

    def all_sunk(self):
        return bool(self.fleet) and len(self.sunk_ships) == len(self.fleet)
