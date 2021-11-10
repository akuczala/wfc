import itertools
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional

import numpy as np

from grid.cell import UncollapsedCell, Cell
from directions import Directions
from grid.grid_boundary import GridBoundary
from propagator import Propagator
from tiles import TileNames, TileData


class Grid(ABC):
    def __init__(self, row_bounds, col_bounds, boundary: GridBoundary, tile_data: Dict[TileNames, TileData],
                 init_cell_factory=None):
        self.row_bounds = row_bounds
        self.col_bounds = col_bounds
        self.boundary = boundary
        self.tile_data = tile_data
        if init_cell_factory is None:
            init_cell_factory = lambda: UncollapsedCell(self.tile_data, {*self.tile_data.keys()})
        self.populate_grid(init_cell_factory)
        self.constrain_boundary()

    @abstractmethod
    def populate_grid(self, init_cell_factory):
        pass

    @abstractmethod
    def get_cell(self, i: int, j: int) -> Cell:
        pass

    @abstractmethod
    def set_cell(self, i: int, j: int, cell: Cell):
        pass

    def constrain_boundary(self):
        for (i, j) in itertools.chain(
                itertools.product([self.row_bounds[0] - 1, self.row_bounds[1]], self.col_iterator),
                itertools.product(self.row_iterator, [self.col_bounds[0] - 1, self.col_bounds[1]])
        ):
            Propagator(self).constrain(i, j)

    def local_collapse(self, i, j):
        self.set_cell(self.get_cell(i, j).collapse())
        for direction, npos in self.get_neighbor_dict(i, j):
            compatible_tiles = self.get_cell(i, j).get_compatible_tiles(direction)
            self.get_cell(*npos).constrain(compatible_tiles)

    def propagated_collapse(self, i, j):
        self.set_cell(i, j, self.get_cell(i, j).collapse())
        Propagator(self).propagate_from(i, j)

    def collapse(self, i, j):
        return self.propagated_collapse(i, j)

    def min_entropy_collapse(self):
        for _ in self.min_entropy_pos_iterator:
            self.collapse(*minpos)

    def scanline_collapse(self):
        for pos in self.pos_iterator:
            self.collapse(*pos)

    @property
    def row_iterator(self):
        return range(self.row_bounds[0], self.row_bounds[1])

    @property
    def col_iterator(self):
        return range(self.col_bounds[0], self.col_bounds[1])

    @property
    def pos_iterator(self):
        return itertools.product(self.row_iterator, self.col_iterator)

    @property
    def width(self):
        return self.row_bounds[1] - self.row_bounds[0]

    @property
    def height(self):
        return self.col_bounds[1] - self.col_bounds[0]

    def neighbor(self, i, j, direction: Directions) -> Optional[Tuple[int, int]]:
        delta_pos = i + direction.value[0], j + direction.value[1]
        if self.in_bounds(*delta_pos):
            return delta_pos
        else:
            return self.boundary.map_pos(self, *delta_pos)

    def get_neighbor_dict(self, i: int, j: int) -> Dict[Directions, Tuple[int, int]]:
        return {
            d: pos
            for d, pos in
            ((d, self.neighbor(i, j, d)) for d in Directions)
            if pos is not None
        }

    def in_bounds(self, i, j) -> bool:
        return self.row_bounds[0] <= i < self.row_bounds[1] and self.col_bounds[0] <= j < self.col_bounds[1]

    def min_entropy_pos(self):
        pos, min_entropy = min(
            ((pos, entropy)
             for pos, entropy in ((pos, self.get_cell(*pos).entropy()) for pos in self.pos_iterator)
             if entropy > 0),
            key=lambda tup: tup[1], default=((0, 0), 0))
        return pos, min_entropy

    @property
    def min_entropy_pos_iterator(self):
        def min_pos_gen():
            while True:
                pos, min_entropy = self.min_entropy_pos()
                if min_entropy == 0:
                    break
                yield pos
        return iter(min_pos_gen())

    def print(self):
        for i in self.row_iterator:
            print("".join([repr(self.get_cell(i, j)) for j in range(self.height)]))

    def print_entropy(self):
        for i in self.row_iterator:
            print("".join(["{:>2}|".format(self.get_cell(i, j).entropy()) for j in range(self.height)]))
