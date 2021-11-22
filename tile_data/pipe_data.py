from typing import Dict

import numpy as np

from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import GeneratedGroup
from symmetry.planar_groups import PlanarGroupAction
from tile_data.connectors import PipeProtoConnectors
from tiles.data import TileConstraints
from tiles.graphics import TileGraphics, TilePixels
from tiles.names import ProtoTileNames
from tileset import TileSet


class PipeProtoTileNames(ProtoTileNames):
    EMPTY = ' '
    HORIZONTAL_PIPE = '-'
    CROSS_PIPE = '+'
    ANGLE_PIPE = 'a'
    TERMINAL = 't'


_rectangular_symmetry = GeneratedGroup({PlanarGroupAction.flip_x(), PlanarGroupAction.flip_y()})
_diagonal_symmetry = GeneratedGroup({PlanarGroupAction.swap_xy()})


class PipeTileSet(TileSet):
    SYM_PROTO_TILE_NAMES_ENUM_NAME = "SymPipeProtoTileNames"
    proto_tile_name_enum = PipeProtoTileNames
    proto_connector_enum = PipeProtoConnectors

    @property
    def tile_symmetries(self):
        return {}

    def get_symmetry_generators(self):
        return self.symmetry_generators_from_constraints()

    @property
    def connector_symmetries(self):
        return {
            self.proto_connector_enum.NONE: None,
            self.proto_connector_enum.HORIZONTAL: _rectangular_symmetry
        }

    @property
    def tile_constraints(self):
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        no_con, hz_con = connector_dict[self.proto_connector_enum.NONE], connector_dict[
            self.proto_connector_enum.HORIZONTAL]
        vt_con = hz_con.transform(PlanarGroupAction.rot90())
        return {
            PipeProtoTileNames.EMPTY: TileConstraints.make_constraints_2d(
                up=no_con,
                down=no_con,
                left=no_con,
                right=no_con
            ),
            PipeProtoTileNames.HORIZONTAL_PIPE: TileConstraints.make_constraints_2d(
                up=no_con,
                down=no_con,
                left=hz_con,
                right=hz_con
            ),
            PipeProtoTileNames.CROSS_PIPE: TileConstraints.make_constraints_2d(
                up=vt_con,
                down=vt_con,
                left=hz_con,
                right=hz_con
            ),
            PipeProtoTileNames.ANGLE_PIPE: TileConstraints.make_constraints_2d(
                up=vt_con,
                down=no_con,
                left=no_con,
                right=hz_con,
            ),
            PipeProtoTileNames.TERMINAL: TileConstraints.make_constraints_2d(
                up=vt_con,
                down=no_con,
                left=no_con,
                right=no_con,
            )
        }

    @property
    def tile_weights(self):
        return {
            PipeProtoTileNames.EMPTY: 3,
            PipeProtoTileNames.HORIZONTAL_PIPE: 3,
            PipeProtoTileNames.CROSS_PIPE: 1,
            PipeProtoTileNames.ANGLE_PIPE: 1,
            PipeProtoTileNames.TERMINAL: 0.01
        }

    @property
    def tile_graphics(self) -> Dict[ProtoTileNames, TileGraphics]:
        return {k: TilePixels(v) for k, v in {
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
