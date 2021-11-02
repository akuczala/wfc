import numpy as np

from tiles import random_tile


class Cell:
    def __init__(self, tile_data):
        self.tile_data = tile_data

    def entropy(self):
        pass

    def collapse(self):
        pass

    def constrain(self, tiles):
        pass

    def get_compatible_tiles(self, direction):
        pass

    def get_pixels(self) -> np.ndarray:
        pass


class UncollapsedCell(Cell):
    def __init__(self, tile_data, tiles):
        super().__init__(tile_data)
        self.tiles = tiles

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

    def get_pixels(self) -> np.ndarray:
        return np.mean([self.tile_data[t].pixels for t in self.tiles],axis=0)


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

    def get_pixels(self) -> np.ndarray:
        return self.tile_data[self.tile].pixels

    @property
    def tiles(self):
        return {self.tile}

    def __repr__(self):
        return self.tile.value
