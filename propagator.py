from typing import List, Tuple


class Propagator:
    def __init__(self, grid: "Grid"):
        self.stack: List[Tuple[int, int]] = []
        self.grid = grid

    def constrain(self, i: int, j: int):
        # print(i,j)
        for direction, npos in self.grid.get_neighbor_dict(i, j).items():
            compatible_tiles = self.grid.get_cell(i, j).get_compatible_tiles(direction)
            prev_len = len(self.grid.get_cell(*npos).tiles)
            self.grid.set_cell(*npos, self.grid.get_cell(*npos).constrain(compatible_tiles))
            new_len = len(self.grid.get_cell(*npos).tiles)
            if new_len != prev_len:
                # print(f'add {(ni, nj)} to stack')
                self.stack.append(npos)

    def propagate_from(self, i, j):
        self.stack = [(i, j)]
        while len(self.stack) > 0:
            self.constrain(*self.stack.pop())
            # print(self.stack)
