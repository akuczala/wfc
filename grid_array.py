import numpy as np

from cell import UncollapsedCell, Cell
from grid import Grid
from grid_boundary import GridBoundary


class GridArray(Grid):
    def __init__(self, width: int, height: int, boundary: GridBoundary, tile_data, init_cell_factory=None):
        super().__init__((0, width), (0, height), boundary, tile_data, init_cell_factory)
        self.cells: np.ndarray


    def populate_grid(self, init_cell_factory):
        self.cells = np.array([
            [
                init_cell_factory() for y in self.col_iterator
            ] for x in self.row_iterator
        ])

    def get_cell(self, i: int, j: int) -> Cell:
        if self.in_bounds(i, j):
            return self.cells[i, j]
        else:
            return self.boundary.get_cell(self, i, j)

    def set_cell(self, i: int, j: int, cell: Cell):
        if self.in_bounds(i, j):
            self.cells[i, j] = cell
        else:
            raise ValueError(f"Cannot set cell {i},{j}")

    def synthesize_img(self):
        return np.concatenate([
            np.concatenate([c.get_pixels() for c in row], axis=1)
            for row in self.cells], axis=0
        )