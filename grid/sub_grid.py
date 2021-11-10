from typing import Tuple

from grid.cell import Cell
from grid.grid import Grid
from grid.grid_boundary import SuperGridBoundary


class SubGrid(Grid):

    def __init__(self, super_grid: Grid, pos: Tuple[int, int], size: Tuple[int, int], tile_data, init_cell_factory):
        self.super_grid = super_grid
        self.pos = pos
        self.size = size
        super().__init__(
            (pos[0], pos[0] + size[0]),
            (pos[1], pos[1] + size[1]),
            SuperGridBoundary(),
            tile_data,
            init_cell_factory
        )


    def populate_grid(self, init_cell_factory):
        for (i, j) in self.pos_iterator:
            self.set_cell(i, j, init_cell_factory())

    def get_cell(self, i: int, j: int) -> Cell:
        if self.in_bounds(i, j):
            return self.super_grid.get_cell(i, j)
        else:
            return self.boundary.get_cell(self, i, j)

    def set_cell(self, i: int, j: int, cell: Cell):
        if self.in_bounds(i, j):
            self.super_grid.set_cell(i, j, cell)
        else:
            raise ValueError(f"Cannot set cell {i},{j}")