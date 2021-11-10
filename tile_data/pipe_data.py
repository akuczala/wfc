import numpy as np

from directions import Directions
from symmetry.groups import Trivial, Z2, Group, Z4_SQUARE
from tile_data.connectors import PipeConnectors
from tiles import ProtoTileNames
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
        PipeProtoTileNames.ANGLE_PIPE: Z4_SQUARE,
        PipeProtoTileNames.TERMINAL: Z4_SQUARE,
    }
    tile_constraints = {
        PipeProtoTileNames.EMPTY: {
            Directions.UP: PipeConnectors.NONE,
            Directions.DOWN: PipeConnectors.NONE,
            Directions.LEFT: PipeConnectors.NONE,
            Directions.RIGHT: PipeConnectors.NONE,
        },
        PipeProtoTileNames.HORIZONTAL_PIPE: {
            Directions.UP: PipeConnectors.NONE,
            Directions.DOWN: PipeConnectors.NONE,
            Directions.LEFT: PipeConnectors.HORIZONTAL,
            Directions.RIGHT: PipeConnectors.HORIZONTAL,
        },
        PipeProtoTileNames.CROSS_PIPE: {
            Directions.UP: PipeConnectors.VERTICAL,
            Directions.DOWN: PipeConnectors.VERTICAL,
            Directions.LEFT: PipeConnectors.HORIZONTAL,
            Directions.RIGHT: PipeConnectors.HORIZONTAL,
        },
        PipeProtoTileNames.ANGLE_PIPE: {
            Directions.UP: PipeConnectors.VERTICAL,
            Directions.DOWN: PipeConnectors.NONE,
            Directions.LEFT: PipeConnectors.NONE,
            Directions.RIGHT: PipeConnectors.HORIZONTAL,
        },
        PipeProtoTileNames.TERMINAL: {
            Directions.UP: PipeConnectors.VERTICAL,
            Directions.DOWN: PipeConnectors.NONE,
            Directions.LEFT: PipeConnectors.NONE,
            Directions.RIGHT: PipeConnectors.NONE,
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

