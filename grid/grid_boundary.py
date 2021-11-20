from abc import ABC, abstractmethod
from typing import Tuple, Optional

from grid.cell import Cell
from grid.pos import Pos


class GridBoundary(ABC):

    @abstractmethod
    def get_cell(self, grid, pos: Pos) -> Cell:
        pass

    @abstractmethod
    def map_pos(self, grid, pos: Pos) -> Optional[Pos]:
        pass

    @staticmethod
    def error_if_in_bounds(grid, pos: Pos):
        if grid.in_bounds(pos):
            raise ValueError(f"Cell {pos} not outside grid!")


class PeriodicGridBoundary(GridBoundary):

    def map_pos(self, grid, pos: Pos) -> Optional[Pos]:
        pos0 = [bounds[0] for bounds in grid.index_bounds]
        return tuple((i - i0) % length for i, i0, length in zip(pos, pos0, grid.shape))

    def get_cell(self, grid, pos: Pos) -> Cell:
        return grid.get_cell(self.map_pos(grid, pos))


class ConstantGridBoundary(GridBoundary):
    def map_pos(self, grid, pos: Pos) -> Optional[Tuple[int, int]]:
        self.error_if_in_bounds(grid, pos)
        return None

    def __init__(self, boundary_cell):
        self.boundary_cell = boundary_cell

    def get_cell(self, grid, pos: Pos) -> Cell:
        self.error_if_in_bounds(grid, pos)
        return self.boundary_cell


class SuperGridBoundary(GridBoundary):

    def map_pos(self, grid, pos: Pos) -> Optional[Pos]:
        self.error_if_in_bounds(grid, pos)
        #return pos
        return None

    def get_cell(self, grid, pos: Pos) -> Cell:
        self.error_if_in_bounds(grid, pos)
        return grid.super_grid.get_cell(pos)