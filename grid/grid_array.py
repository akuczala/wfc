from typing import Tuple

import numpy as np

from grid.cell import Cell
from grid.grid import Grid
from grid.grid_boundary import GridBoundary
from grid.pos import Pos


class GridArray(Grid):
    def __init__(self, shape: Tuple[int, ...], boundary: GridBoundary, tile_data, init_cell_factory=None):
        super().__init__(tuple((0, s) for s in shape), boundary, tile_data, init_cell_factory)
        self.cells: np.ndarray

    def populate_grid(self, init_cell_factory):
        self.cells = np.array([init_cell_factory() for _ in self.pos_iterator]).reshape(self.shape)

    def get_cell(self, pos: Pos) -> Cell:
        if self.in_bounds(pos):
            return self.cells[pos]
        else:
            return self.boundary.get_cell(self, pos)

    def set_cell(self, pos: Pos, cell: Cell):
        if self.in_bounds(pos):
            self.cells[pos] = cell
        else:
            raise ValueError(f"Cannot set cell {pos}")

    def synthesize_img(self):
        return np.concatenate([
            np.concatenate([c.get_pixels() for c in row], axis=1)
            for row in self.cells], axis=0
        )
