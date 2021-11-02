from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set

import numpy as np

from connectors import Connectors
from directions import Directions


class ProtoTileNames(Enum):

    def get_all_tiles(self):
        return {t for t in self}


@dataclass
class ProtoTileData:
    constraints: Dict[Directions, Connectors]
    weight: float
    name: ProtoTileNames
    pixels: np.array

def random_tile(tile_data, tiles):
    tile_list = list(tiles)
    probs = np.array([tile_data[t].weight for t in tile_list])
    probs = probs / sum(probs)
    return np.random.choice(tile_list, p=probs)


class TileNames:
    pass

# not allowed to extend nonempty enumerations
# class PipeTileNames(TileNames, PipeProtoTileNames):
#     pass


@dataclass
class TileData:
    name: TileNames
    weight: float
    compatible_tiles: Dict[Directions, Set[TileNames]]
    pixels: Set[TileNames]


