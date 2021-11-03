import itertools
from typing import Dict, Tuple

import numpy as np

from cell import UncollapsedCell, Cell
from directions import Directions
from propagator import Propagator
from tiles import TileNames, TileData


class Grid:
    def __init__(self, width: int, height: int, tile_data, periodic):
        self.periodic = False
        self.width = width
        self.height = height
        self.tile_data: Dict[TileNames, TileData] = tile_data
        self.cells = np.array([
            [
                UncollapsedCell(tile_data, {*self.tile_data.keys()}) for y in range(height)
            ] for x in range(width)
        ])
        # if not self.periodic:
        #     for (i, j) in itertools.product(range(self.width), (0, self.height - 1)):
        #         self.propagated_collapse(i, j)
        #     for (i, j) in itertools.product((0, self.width - 1),range(self.height)):
        #         self.propagated_collapse(i, j)


    def get_cell(self, i: int, j: int) -> Cell:
        return self.cells[i, j]  # todo boundary conditions

    def local_collapse(self, i, j):
        self.cells[i, j] = self.get_cell(i, j).collapse()
        for direction in Directions:
            compatible_tiles = self.get_cell(i, j).get_compatible_tiles(direction)
            ni, nj = self.neighbor(i, j, direction)
            self.get_cell(ni, nj).constrain(compatible_tiles)

    def propagated_collapse(self, i, j):
        self.cells[i, j] = self.get_cell(i, j).collapse()
        Propagator(self).propagate_from(i, j)

    def collapse(self, i, j):
        return self.propagated_collapse(i, j)

    def collapse_all(self):
        for _ in range(self.width * self.height):
            minpos, min_val = self.min_entropy_pos()
            if min_val == 0:
                break
            self.collapse(*minpos)

    def get_periodic(self, i, j):
        return (i % self.width), (j % self.height)

    def in_bounds(self, i: int, j: int) -> bool:
        return (0 <= i < self.width) and (0 <= j < self.height)

    def neighbor(self, i, j, direction: Directions):
        if self.periodic:
            return self.get_periodic(i + direction.value[0], j + direction.value[1])
        else:
            return i + direction.value[0], j + direction.value[1]


    def get_neighbor_dict(self, i: int, j: int) -> Dict[Directions, Tuple[int, int]]:
        return {
            d: pos
            for d, pos in
            ((d, self.neighbor(i, j, d)) for d in Directions)
            if self.in_bounds(*pos)
        }

    def min_entropy_pos(self):
        idx, min_entropy = min(
            ((i, entropy)
             for i, entropy in enumerate(cell.entropy() for cell in self.cells.ravel())
             if entropy > 0),
            key=lambda tup: tup[1], default=(0, 0))
        return np.unravel_index(idx, self.cells.shape), min_entropy

    def print(self):
        for i in range(self.width):
            print("".join([repr(self.get_cell(i, j)) for j in range(self.height)]))

    def print_entropy(self):
        for i in range(self.width):
            print("".join(["{:>2}|".format(self.get_cell(i, j).entropy()) for j in range(self.height)]))

    def synthesize_img(self):
        return np.concatenate([
            np.concatenate([c.get_pixels() for c in row], axis=1)
            for row in self.cells], axis=0
        )