from enum import auto

import numpy as np
from matplotlib import pyplot as plt

from directions import Directions
from symmetry import Trivial, Group, Z4, D4
from tile_data.connectors import DirectedPipeConnectors
from tiles import ProtoTileNames
from tileset import TileSet

ConnectorsEnum = DirectedPipeConnectors

class DirectedProtoTileNames(ProtoTileNames):
    EMPTY = 'EMPTY'
    PIPE = 'PIPE'
    CROSS_PIPE = 'CROSS_PIPE'
    ANGLE_PIPE = 'ANGLE_PIPE'
    EMITTER = 'EMITTER'
    CONSUMER = 'CONSUMER'


def generate_tile_pixels():
    img = plt.imread('assets/directed_pipe_tiles.png')
    arr = img[:, :, 0]
    s = 16

    def end_tile(i):
        return i + s - 1

    def extract_tile(i, j):
        return arr[i:end_tile(i), j:end_tile(j)]

    return {
        name: extract_tile(s * i, s * j) for name, (i, j) in {
            DirectedProtoTileNames.PIPE: (0, 0),
            DirectedProtoTileNames.ANGLE_PIPE: (0, 1),
            DirectedProtoTileNames.CROSS_PIPE: (0, 2),
            DirectedProtoTileNames.EMPTY: (0, 3),
            DirectedProtoTileNames.EMITTER: (1, 0),
            DirectedProtoTileNames.CONSUMER: (1, 1),
        }.items()
    }


class DirectedPipeTileSet(TileSet):
    SYM_PROTO_TILE_NAMES_ENUM_NAME = "SymDirectedProtoTileNames"
    proto_tile_name_enum = DirectedProtoTileNames
    tile_symmetries = {
        proto_tile_name_enum.EMPTY: Trivial(),
        proto_tile_name_enum.PIPE: Z4(Group.rot90()),
        proto_tile_name_enum.CROSS_PIPE: Z4(Group.rot90()), # todo check this symmetry
        proto_tile_name_enum.ANGLE_PIPE: D4(Group.rot90(), Group.flip_x()),
        proto_tile_name_enum.EMITTER: Z4(Group.rot90()),
        proto_tile_name_enum.CONSUMER: Z4(Group.rot90()),
    }
    tile_constraints = {
        proto_tile_name_enum.EMPTY: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.NONE,
        },
        proto_tile_name_enum.PIPE: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.RIGHT,
            Directions.RIGHT: ConnectorsEnum.RIGHT,
        },
        proto_tile_name_enum.CROSS_PIPE: {
            Directions.UP: ConnectorsEnum.UP,
            Directions.DOWN: ConnectorsEnum.UP,
            Directions.LEFT: ConnectorsEnum.RIGHT,
            Directions.RIGHT: ConnectorsEnum.RIGHT,
        },
        proto_tile_name_enum.ANGLE_PIPE: {
            Directions.UP: ConnectorsEnum.UP,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.LEFT,
        },
        proto_tile_name_enum.EMITTER: {
            Directions.UP: ConnectorsEnum.UP,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.NONE,
        },
        proto_tile_name_enum.CONSUMER: {
            Directions.UP: ConnectorsEnum.DOWN,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.NONE,
        }
    }
    tile_weights = {
        proto_tile_name_enum.EMPTY: 80,
        proto_tile_name_enum.PIPE: 3,
        proto_tile_name_enum.CROSS_PIPE: 0.1,
        proto_tile_name_enum.ANGLE_PIPE: 0.5,
        proto_tile_name_enum.EMITTER: 0.0,
        proto_tile_name_enum.CONSUMER: 0.0

    }
    tile_imgs = generate_tile_pixels()

    def __init__(self):
        super().__init__()

