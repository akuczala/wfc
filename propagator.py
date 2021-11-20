from typing import List, Tuple

from grid.grid import Pos


class Propagator:
    def __init__(self, grid: "Grid"):
        self.stack: List[Pos] = []
        self.grid = grid

    def constrain(self, pos: Pos):
        for direction, npos in self.grid.get_neighbor_dict(pos).items():
            compatible_tiles = self.grid.get_cell(pos).get_compatible_tiles(direction)
            prev_len = len(self.grid.get_cell(npos).tiles)
            self.grid.set_cell(npos, self.grid.get_cell(npos).constrain(compatible_tiles))
            new_len = len(self.grid.get_cell(npos).tiles)
            if new_len != prev_len:
                self.stack.append(npos)

    def propagate_from(self, pos: Pos):
        self.stack = [pos]
        while len(self.stack) > 0:
            self.constrain(self.stack.pop())
            # print(self.stack)
