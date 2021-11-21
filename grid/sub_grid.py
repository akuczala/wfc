from typing import Tuple, Iterable

from directions import Directions
from grid.cell import Cell
from grid.grid import Grid
from grid.grid_boundary import SuperGridBoundary
from grid.pos import Pos


class SubGrid(Grid):

    def __init__(self, super_grid: Grid, pos: Pos, size: Tuple[int, ...], tile_data, init_cell_factory):
        self.super_grid = super_grid
        self.pos = pos
        self.size = size
        super().__init__(
            tuple((p, p + s) for p, s in zip(pos, size)),
            SuperGridBoundary(),
            tile_data,
            init_cell_factory
        )

    @property
    def directions(self) -> Iterable[Directions]:
        return self.super_grid.directions

    def populate_grid(self, init_cell_factory):
        for pos in self.pos_iterator:
            self.set_cell(pos, init_cell_factory())

    def get_cell(self, pos: Pos) -> Cell:
        if self.in_bounds(pos):
            return self.super_grid.get_cell(pos)
        else:
            return self.boundary.get_cell(self, pos)

    def set_cell(self, pos: Pos, cell: Cell):
        if self.in_bounds(pos):
            self.super_grid.set_cell(pos, cell)
        else:
            raise ValueError(f"Cannot set cell {pos}")
