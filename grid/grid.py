import itertools
from abc import ABC, abstractmethod
from typing import Dict, Optional, Iterable

from grid.cell import UncollapsedCell, Cell
from directions import Directions
from grid.grid_boundary import GridBoundary
from grid.pos import Pos
from propagator import Propagator
from tiles.data import TileData
from tiles.names import TileNames


class Grid(ABC):
    def __init__(self, index_bounds, boundary: GridBoundary, tile_data: Dict[TileNames, TileData],
                 init_cell_factory=None):
        self.index_bounds = index_bounds
        self.boundary = boundary
        self.tile_data = tile_data
        if init_cell_factory is None:
            init_cell_factory = lambda: UncollapsedCell(self.tile_data, {*self.tile_data.keys()})
        self.populate_grid(init_cell_factory)
        self.constrain_boundary()

    @property
    def dim(self):
        return len(self.index_bounds)

    @abstractmethod
    def populate_grid(self, init_cell_factory):
        pass

    @abstractmethod
    def get_cell(self, pos: Pos) -> Cell:
        pass

    @abstractmethod
    def set_cell(self, pos: Pos, cell: Cell):
        pass

    # todo generalize to d dim
    def constrain_boundary(self):
        for pos in itertools.chain(*(
                itertools.product(*(
                        (
                                [self.index_bounds[ax][0] - 1, self.index_bounds[ax][1]] if ax == chained_ax
                                else self.axis_iterator(ax))
                        for ax in range(self.dim)
                )) for chained_ax in range(self.dim))):
            Propagator(self).constrain(pos)

    def local_collapse(self, pos):
        self.set_cell(self.get_cell(pos).collapse())
        for direction, npos in self.get_neighbor_dict(pos):
            compatible_tiles = self.get_cell(pos).get_compatible_tiles(direction)
            self.get_cell(npos).constrain(compatible_tiles)

    def propagated_collapse(self, pos):
        self.set_cell(pos, self.get_cell(pos).collapse())
        Propagator(self).propagate_from(pos)

    def collapse(self, pos):
        return self.propagated_collapse(pos)

    def min_entropy_collapse(self):
        for minpos in self.min_entropy_pos_iterator:
            self.collapse(minpos)

    def scanline_collapse(self):
        for pos in self.pos_iterator:
            self.collapse(pos)

    def axis_iterator(self, axis: int):
        return range(*self.index_bounds[axis])

    @property
    def pos_iterator(self):
        return itertools.product(*(self.axis_iterator(ax) for ax in range(self.dim)))

    @property
    def shape(self):
        return tuple(self.index_bounds[ax][1] - self.index_bounds[ax][0] for ax in range(self.dim))

    @property
    @abstractmethod
    def directions(self) -> Iterable[Directions]:
        pass

    def neighbor(self, pos: Pos, direction: Directions) -> Optional[Pos]:
        delta_pos = tuple(pos_i + direction.value[i] for i, pos_i in enumerate(pos))
        if self.in_bounds(delta_pos):
            return delta_pos
        else:
            return self.boundary.map_pos(self, delta_pos)

    def get_neighbor_dict(self, pos: Pos) -> Dict[Directions, Pos]:
        return {
            d: n_pos
            for d, n_pos in
            ((d, self.neighbor(pos, d)) for d in self.directions)
            if n_pos is not None
        }

    def in_bounds(self, pos: Pos) -> bool:
        return all(self.index_bounds[ax][0] <= x < self.index_bounds[ax][1] for ax, x in enumerate(pos))

    def min_entropy_pos(self):
        pos, min_entropy = min(
            ((pos, entropy)
             for pos, entropy in ((pos, self.get_cell(pos).entropy()) for pos in self.pos_iterator)
             if entropy > 0),
            key=lambda tup: tup[1], default=(tuple(0 for _ in range(self.dim)), 0))
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
        for i in self.axis_iterator(0):
            print("".join([repr(self.get_cell((i, j))) for j in range(self.shape[1])]))

    def print_entropy(self):
        for i in self.axis_iterator(0):
            print("".join(["{:>2}|".format(self.get_cell((i, j)).entropy()) for j in range(self.shape[1])]))
