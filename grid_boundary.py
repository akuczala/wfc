from abc import ABC, abstractmethod
from typing import Tuple, Optional

from cell import Cell
from directions import Directions


class GridBoundary(ABC):

    @abstractmethod
    def get_cell(self, grid, i: int, j: int) -> Cell:
        pass

    @abstractmethod
    def map_pos(self, grid, i: int, j: int) -> Optional[Tuple[int, int]]:
        pass

    @staticmethod
    def error_if_in_bounds(grid, i: int, j: int):
        if grid.in_bounds(i, j):
            raise ValueError(f"Cell {i, j} not outside grid!")


class PeriodicGridBoundary(GridBoundary):

    def map_pos(self, grid, i: int, j: int) -> Optional[Tuple[int, int]]:
        i0, j0 = grid.row_bounds[0], grid.col_bounds[0]
        return (i - i0) % grid.width + i0, (j - j0) % grid.height + j0

    def get_cell(self, grid, i: int, j: int) -> Cell:
        return grid.get_cell(*self.map_pos(grid, i, j))


class ConstantGridBoundary(GridBoundary):
    def map_pos(self, grid, i: int, j: int) -> Optional[Tuple[int, int]]:
        self.error_if_in_bounds(grid, i, j)
        return None


    def __init__(self, boundary_cell):
        self.boundary_cell = boundary_cell

    def get_cell(self, grid, i: int, j: int) -> Cell:
        self.error_if_in_bounds(grid, i, j)
        return self.boundary_cell


class SuperGridBoundary(GridBoundary):

    def map_pos(self, grid, i: int, j: int) -> Optional[Tuple[int, int]]:
        self.error_if_in_bounds(grid, i, j)
        #return i, j
        return None

    def get_cell(self, grid, i: int, j: int) -> Cell:
        self.error_if_in_bounds(grid, i, j)
        return grid.super_grid.get_cell(i, j)