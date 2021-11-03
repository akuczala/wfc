from typing import List, Tuple

from directions import Directions


class Propagator:
    def __init__(self, grid: "Grid"):
        self.stack: List[Tuple[int, int]] = []
        self.grid = grid

    def constrain(self, i: int, j: int):
        # print(i,j)
        for direction, (ni, nj) in self.grid.get_neighbor_dict(i, j).items():
            compatible_tiles = self.grid.get_cell(i, j).get_compatible_tiles(direction)
            prev_len = len(self.grid.get_cell(ni, nj).tiles)
            self.grid.cells[ni, nj] = self.grid.get_cell(ni, nj).constrain(compatible_tiles)
            new_len = len(self.grid.get_cell(ni, nj).tiles)
            if new_len != prev_len:
                # print(f'add {(ni, nj)} to stack')
                self.stack.append((ni, nj))

    def propagate_from(self, i, j):
        self.stack = [(i, j)]
        while len(self.stack) > 0:
            self.constrain(*self.stack.pop())
            # print(self.stack)
