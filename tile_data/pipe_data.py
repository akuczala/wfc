from enum import Enum
from typing import Dict

import numpy as np

from connectors import Connectors
from directions import Directions
from symmetry import Trivial, Z2, Group, Z4, TileSymmetryGenerator
from tiles import ProtoTileNames, ProtoTileData
from tileset import TileSet

class PipeProtoTileNames(ProtoTileNames):
    EMPTY = ' '
    HORIZONTAL_PIPE = '-'
    CROSS_PIPE = '+'
    ANGLE_PIPE = 'a'
    TERMINAL = 't'

class PipeTileSet(TileSet):
    SYM_PROTO_TILE_NAMES_ENUM_NAME = "SymPipeProtoTileNames"
    proto_tile_name_enum = PipeProtoTileNames
    tile_symmetries = {
        PipeProtoTileNames.EMPTY: Trivial(),
        PipeProtoTileNames.HORIZONTAL_PIPE: Z2(Group.swap_xy()),
        PipeProtoTileNames.CROSS_PIPE: Trivial(),
        PipeProtoTileNames.ANGLE_PIPE: Z4(Group.rot90()),
        PipeProtoTileNames.TERMINAL: Z4(Group.rot90()),
    }
    tile_constraints = {
        PipeProtoTileNames.EMPTY: {
            Directions.UP: Connectors.NONE,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.NONE,
        },
        PipeProtoTileNames.HORIZONTAL_PIPE: {
            Directions.UP: Connectors.NONE,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.HORIZONTAL,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.CROSS_PIPE: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.VERTICAL,
            Directions.LEFT: Connectors.HORIZONTAL,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.ANGLE_PIPE: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.TERMINAL: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.NONE,
        }
    }
    tile_weights = {
        PipeProtoTileNames.EMPTY: 80,
        PipeProtoTileNames.HORIZONTAL_PIPE: 3,
        PipeProtoTileNames.CROSS_PIPE: 0.5,
        PipeProtoTileNames.ANGLE_PIPE: 1,
        PipeProtoTileNames.TERMINAL: 0.0
    }
    tile_imgs = {
        PipeProtoTileNames.EMPTY: np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        PipeProtoTileNames.HORIZONTAL_PIPE: np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]),
        PipeProtoTileNames.CROSS_PIPE: np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]),
        PipeProtoTileNames.ANGLE_PIPE: np.array([
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]),
        PipeProtoTileNames.TERMINAL: np.array([
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]),
    }

    def __init__(self):
        super().__init__()

