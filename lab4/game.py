import random

from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        self._place_fleet(self.player)
        self._place_fleet(self.enemy)

    def _place_fleet(self, board):
        for length in (3, 2):
            placements = []
            for row in range(Board.SIZE):
                for column in range(Board.SIZE):
                    for row_step, column_step in ((0, 1), (1, 0)):
                        end_row = row + (length - 1) * row_step
                        end_column = column + (length - 1) * column_step
                        if end_row >= Board.SIZE or end_column >= Board.SIZE:
                            continue
                        cells = {
                            (row + offset * row_step, column + offset * column_step)
                            for offset in range(length)
                        }
                        if not board.ships.intersection(cells):
                            placements.append(cells)
            if not placements:
                raise ValueError("Unable to place the full fleet on this board.")
            board.place_ship(random.choice(placements))

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("    " + " ".join(str(column + 1) for column in range(Board.SIZE)))
        for row in range(Board.SIZE):
            marks = [
                "_" if (row, column) not in self.enemy.shot_results
                else "X" if self.enemy.shot_results[(row, column)]
                else "O"
                for column in range(Board.SIZE)
            ]
            print(f"{row + 1:>2}  " + " ".join(marks))
        print("Ship cells remaining:", len(self.enemy.ships - self.enemy.shots))

    def _report_shot(self, board, pos, shooter):
        sunk_before = board.sunk_ships
        hit = board.fire(pos)
        print(f"{shooter} HIT!" if hit else f"{shooter} MISS!")
        if board.sunk_ships - sunk_before:
            if board.all_sunk():
                print(f"{shooter} sank the fleet.")
            elif shooter == "You":
                print("You sank a ship.")
            else:
                print("AI sank one of your ships.")
        return hit

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue
            if not (0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE):
                print("Outside board.")
                continue
            if pos in self.enemy.shots:
                print("Already fired there.")
                continue
            player_hit = self._report_shot(self.enemy, pos, "You")
            if self.enemy.all_sunk():
                return
            if player_hit:
                continue

            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("AI has no remaining targets.")
                continue
            print(f"AI fired at {ai_pos[0] + 1},{ai_pos[1] + 1}")
            ai_hit = self._report_shot(self.player, ai_pos, "AI")
            self.ai.record_result(ai_pos, ai_hit)
            if self.player.all_sunk():
                return
