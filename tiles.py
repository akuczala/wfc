from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set

import numpy as np

from connectors import Connectors
from directions import Directions


class ProtoTileNames(Enum):

    def get_all_tiles(self):
        return {t for t in self}


class PipeProtoTileNames(ProtoTileNames):
    EMPTY = ' '
    HORIZONTAL_PIPE = '-'
    VERTICAL_PIPE = '|'
    CROSS_PIPE = '+'
    ANGLE_PIPE_1 = 'a'
    ANGLE_PIPE_2 = 'b'
    ANGLE_PIPE_3 = 'c'
    ANGLE_PIPE_4 = 'd'
    TERMINAL = 't'


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


def generate_compatible_tiles(proto_tile_data: Dict[ProtoTileNames, ProtoTileData]):
    tile_name_enum = type(next(iter(proto_tile_data.keys())))
    return {
        tile: TileData(
            name=tile,
            weight=proto_tile_data[tile].weight,
            compatible_tiles={
                direction: get_constraint_compatible_tiles(proto_tile_data, tile, direction)
                for direction in Directions
            },
            pixels=proto_tile_data[tile].pixels
        ) for tile in tile_name_enum
    }


def get_constraint_compatible_tiles(proto_tile_data, this_tile, direction):
    tile_name_enum = type(next(iter(proto_tile_data.keys())))
    connector = proto_tile_data[this_tile].constraints[direction]
    return {tile for tile in tile_name_enum if proto_tile_data[tile].constraints[direction.reverse()] == connector}
