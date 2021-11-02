from typing import Dict

import numpy as np

from cell import UncollapsedCell
from directions import Directions
from propagator import Propagator
from tiles import TileNames, TileData


class Grid:
    def __init__(self, width: int, height: int, tile_data):
        self.width = width
        self.height = height
        self.tile_data: Dict[TileNames, TileData] = tile_data
        self.cells = np.array([
            [
                UncollapsedCell(tile_data, {*self.tile_data.keys()}) for y in range(height)
            ] for x in range(width)
        ])

    def local_collapse(self, i, j):
        self.cells[i, j] = self.cells[i, j].collapse()
        for direction in Directions:
            compatible_tiles = self.cells[i, j].get_compatible_tiles(direction)
            ni, nj = self.neighbor(i, j, direction)
            self.cells[ni, nj].constrain(compatible_tiles)

    def propagated_collapse(self, i, j):
        self.cells[i, j] = self.cells[i, j].collapse()
        Propagator(self).propagate_from(i, j)

    def collapse(self, i, j):
        return self.propagated_collapse(i, j)

    def collapse_all(self):
        for _ in range(self.width * self.height):
            minpos, min_val = self.min_entropy_pos()
            if min_val == 0:
                break
            self.collapse(*minpos)

    def periodic(self, i, j):
        return (i % self.width), (j % self.height)

    def neighbor(self, i, j, direction):
        return self.periodic(i + direction.value[0], j + direction.value[1])

    def neighbors(self, i, j):
        return [self.neighbor(i, j, d) for d in Directions]

    def min_entropy_pos(self):
        idx, min_entropy = min(
            ((i, entropy)
             for i, entropy in enumerate(cell.entropy() for cell in self.cells.ravel())
             if entropy > 0),
            default=(0, 0))
        return np.unravel_index(idx, self.cells.shape), min_entropy

    def print(self):
        for i in range(self.width):
            print("".join([repr(self.cells[i, j]) for j in range(self.height)]))