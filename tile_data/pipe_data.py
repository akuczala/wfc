import numpy as np

from connectors import GeneratedConnector
from directions import Directions
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Trivial, Z2, Group, Z4_SQUARE
from tile_data.connectors import PipeConnectors, PipeProtoConnectors
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
    SYM_PROTO_CONNECTOR_ENUM = "SymPipeProtoConnectors"
    proto_tile_name_enum = PipeProtoTileNames
    proto_connector_enum = PipeProtoConnectors
    tile_symmetries = {
        PipeProtoTileNames.EMPTY: Trivial(),
        PipeProtoTileNames.HORIZONTAL_PIPE: Z2(Group.swap_xy()),
        PipeProtoTileNames.CROSS_PIPE: Trivial(),
        PipeProtoTileNames.ANGLE_PIPE: Z4_SQUARE,
        PipeProtoTileNames.TERMINAL: Z4_SQUARE,
    }
    # connector_symmetries = ConnectorSymmetryGenerator({
    #     PipeProtoConnectors.NONE: Trivial(),
    #     PipeProtoConnectors.HORIZONTAL: Z2(Group.swap_xy())
    # })
    # connector_enum = connector_symmetries.connector_enum
    # no_con = connector_symmetries.get(proto_connector_enum.NONE, Group.id())
    # hz_con = connector_symmetries.get(proto_connector_enum.HORIZONTAL, Group.id())
    # vt_con = connector_symmetries.get(proto_connector_enum.HORIZONTAL, Group.swap_xy())
    no_con = GeneratedConnector(proto_connector_enum.NONE, Group.id())
    hz_con = GeneratedConnector(proto_connector_enum.HORIZONTAL, Group.id())
    vt_con = GeneratedConnector(proto_connector_enum.HORIZONTAL, Group.swap_xy())
    tile_constraints = {
        PipeProtoTileNames.EMPTY: {
            Directions.UP: no_con,
            Directions.DOWN: no_con,
            Directions.LEFT: no_con,
            Directions.RIGHT: no_con,
        },
        PipeProtoTileNames.HORIZONTAL_PIPE: {
            Directions.UP: no_con,
            Directions.DOWN: no_con,
            Directions.LEFT: hz_con,
            Directions.RIGHT: hz_con
        },
        PipeProtoTileNames.CROSS_PIPE: {
            Directions.UP: vt_con,
            Directions.DOWN: vt_con,
            Directions.LEFT: hz_con,
            Directions.RIGHT: hz_con
        },
        PipeProtoTileNames.ANGLE_PIPE: {
            Directions.UP: vt_con,
            Directions.DOWN: no_con,
            Directions.LEFT: no_con,
            Directions.RIGHT: hz_con,
        },
        PipeProtoTileNames.TERMINAL: {
            Directions.UP: vt_con,
            Directions.DOWN: no_con,
            Directions.LEFT: no_con,
            Directions.RIGHT: no_con,
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

