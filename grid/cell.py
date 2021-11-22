from abc import ABC, abstractmethod
from typing import Set

import numpy as np

from tiles.data import random_tile
from tiles.graphics import TileGraphics, TilePixels
from tiles.names import TileNames
from tileset import TileSet


class Cell(ABC):
    def __init__(self, tile_data):
        self.tile_data = tile_data

    @abstractmethod
    def entropy(self):
        pass

    @abstractmethod
    def collapse(self):
        pass

    @abstractmethod
    def constrain(self, tiles):
        pass

    @abstractmethod
    def get_compatible_tiles(self, direction):
        pass

    @abstractmethod
    def get_graphics(self) -> TileGraphics:
        pass


class UncollapsedCell(Cell):
    def __init__(self, tile_data, tiles):
        super().__init__(tile_data)
        self.tiles = tiles

    @classmethod
    def with_any_tile(cls, tileset: TileSet):
        return UncollapsedCell(tileset.tile_data, {t for t in tileset.tile_name_enum})

    @classmethod
    def excluding_tiles(cls, tileset: TileSet, excluded_tiles: Set[TileNames]):
        tiles = {t for t in tileset.tile_name_enum}.difference(excluded_tiles)
        return UncollapsedCell(tileset.tile_data, tiles)

    @classmethod
    def excluding_weight_zero(cls, tileset: TileSet):
        tiles = {t for t in tileset.tile_name_enum if tileset.tile_data[t].weight > 0}
        return UncollapsedCell(tileset.tile_data, tiles)

    def entropy(self):
        return len(self.tiles)

    def collapse(self):
        return CollapsedCell(self.tile_data, random_tile(self.tile_data, self.tiles))

    def constrain(self, tiles):
        self.tiles = self.tiles.intersection(tiles)
        if len(self.tiles) == 0:
            raise Exception("Unsatisfiable configuration")
        if len(self.tiles) == 1:
            return CollapsedCell(self.tile_data, [t for t in self.tiles][0])
        return self

    def get_compatible_tiles(self, direction):
        return set().union(*(self.tile_data[t].compatible_tiles[direction] for t in self.tiles))

    def __repr__(self):
        return str(self.entropy())

    # todo generalize beyond tile pixels
    def get_graphics(self) -> TileGraphics:
        return TilePixels(np.mean([self.tile_data[t].graphics.array for t in self.tiles], axis=0))


class CollapsedCell(Cell):
    def __init__(self, tile_data, tile):
        super().__init__(tile_data)
        self.tile = tile

    def entropy(self):
        return 0

    def collapse(self):
        return self

    def constrain(self, tiles):
        if self.tile not in tiles:
            raise Exception("Unsatisfiable configuration")
        return self

    def get_compatible_tiles(self, direction):
        return self.tile_data[self.tile].compatible_tiles[direction]

    def get_graphics(self) -> TileGraphics:
        return self.tile_data[self.tile].graphics

    @property
    def tiles(self):
        return {self.tile}

    def __repr__(self):
        return self.tile.value
