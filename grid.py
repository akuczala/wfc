import itertools
from typing import Dict

import numpy as np

from cell import UncollapsedCell, Cell
from directions import Directions
from propagator import Propagator
from tiles import TileNames, TileData


class Grid:
    def __init__(self, width: int, height: int, tile_data, init_cell_factory=None):
        self.width = width
        self.height = height
        self.tile_data: Dict[TileNames, TileData] = tile_data
        if init_cell_factory is None:
            init_cell_factory = lambda: UncollapsedCell(self.tile_data, {*self.tile_data.keys()})
        self.cells = np.array([
            [
                init_cell_factory() for y in range(height)
            ] for x in range(width)
        ])

    def get_cell(self, i: int, j: int) -> Cell:
        return self.cells[i, j]  # todo boundary conditions

    def local_collapse(self, i, j):
        self.cells[i, j] = self.get_cell(i, j).collapse()
        for direction in Directions:
            compatible_tiles = self.get_cell(i, j).get_compatible_tiles(direction)
            ni, nj = self.neighbor(i, j, direction)
            self.get_cell(i, j).constrain(compatible_tiles)

    def propagated_collapse(self, i, j):
        self.cells[i, j] = self.get_cell(i, j).collapse()
        Propagator(self).propagate_from(i, j)

    def collapse(self, i, j):
        return self.propagated_collapse(i, j)

    def min_entropy_collapse(self):
        for _ in range(self.width * self.height):
            minpos, min_val = self.min_entropy_pos()
            if min_val == 0:
                break
            self.collapse(*minpos)

    def scanline_collapse(self):
        for pos in self.pos_iterator:
            self.collapse(*pos)

    @property
    def pos_iterator(self):
        return itertools.product(range(self.width),range(self.height))

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