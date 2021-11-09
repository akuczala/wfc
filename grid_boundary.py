from abc import ABC, abstractmethod

from cell import Cell


class GridBoundary(ABC):

    @abstractmethod
    def get_cell(self, grid, i: int, j: int) -> Cell:
        pass


class PeriodicGridBoundary(GridBoundary):

    def get_cell(self, grid, i: int, j: int) -> Cell:
        return grid.get_cell(i % grid.width, j % grid.height)


class ConstantBoundary(GridBoundary):
    def __init__(self, boundary_cell):
        self.boundary_cell = boundary_cell

    def get_cell(self, grid, i: int, j: int) -> Cell:
        if grid.in_bounds(i, j):
            raise ValueError(f"Cell {i,j} not outside grid!")
        return self.boundary_cell


class SuperGridBoundary(GridBoundary):

    def get_cell(self, grid, i: int, j: int) -> Cell:
        if grid.in_bounds(i, j):
            raise ValueError(f"Cell {i,j} not outside grid!")
        return grid.super_grid.get_cell(i, j)