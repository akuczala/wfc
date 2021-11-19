import numpy as np

from directions import Directions
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Group, GeneratedGroup
from tile_data.connectors import PipeProtoConnectors
from tiles import ProtoTileNames, TilePixels, TileConstraints
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
    proto_connector_enum = PipeProtoConnectors
    _rectangular_symmetry = GeneratedGroup({Group.flip_x(), Group.flip_y()})
    _diagonal_symmetry = GeneratedGroup({Group.swap_xy()})
    # todo generate tile symmetries from connector symmetries?
    tile_symmetries = {
        PipeProtoTileNames.EMPTY: None,
        PipeProtoTileNames.HORIZONTAL_PIPE: _rectangular_symmetry,
        PipeProtoTileNames.CROSS_PIPE: None,
        PipeProtoTileNames.ANGLE_PIPE: _diagonal_symmetry,
        PipeProtoTileNames.TERMINAL: GeneratedGroup({Group.flip_y()}),
    }
    connector_symmetries = {
        proto_connector_enum.NONE: None,
        proto_connector_enum.HORIZONTAL: _rectangular_symmetry
    }
    connector_dict = ConnectorSymmetryGenerator(connector_symmetries).make_base_connector_dict()
    no_con, hz_con = connector_dict[proto_connector_enum.NONE], connector_dict[proto_connector_enum.HORIZONTAL]
    vt_con = hz_con.transform(Group.rot90())
    tile_constraints = {
        PipeProtoTileNames.EMPTY: TileConstraints.make_constraints(
            up=no_con,
            down=no_con,
            left=no_con,
            right=no_con
        ),
        PipeProtoTileNames.HORIZONTAL_PIPE: TileConstraints.make_constraints(
            up=no_con,
            down=no_con,
            left=hz_con,
            right=hz_con
        ),
        PipeProtoTileNames.CROSS_PIPE: TileConstraints.make_constraints(
            up=vt_con,
            down=vt_con,
            left=hz_con,
            right=hz_con
        ),
        PipeProtoTileNames.ANGLE_PIPE: TileConstraints.make_constraints(
            up=vt_con,
            down=no_con,
            left=no_con,
            right=hz_con,
        ),
        PipeProtoTileNames.TERMINAL: TileConstraints.make_constraints(
            up=vt_con,
            down=no_con,
            left=no_con,
            right=no_con,
        )
    }
    tile_weights = {
        PipeProtoTileNames.EMPTY: 80,
        PipeProtoTileNames.HORIZONTAL_PIPE: 3,
        PipeProtoTileNames.CROSS_PIPE: 0.5,
        PipeProtoTileNames.ANGLE_PIPE: 1,
        PipeProtoTileNames.TERMINAL: 0.01
    }
    tile_imgs = {k: TilePixels(v) for k, v in {
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
    }.items()}

    def __init__(self):
        super().__init__()

