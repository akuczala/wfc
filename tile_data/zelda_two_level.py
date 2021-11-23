from enum import auto
from typing import Dict

from matplotlib import pyplot as plt

from connectors import ProtoConnectors
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Group, GeneratedGroup
from tile_data.connectors import Zelda2ProtoConnectors
from tiles.data import TileConstraints
from tiles.graphics import TilePixels
from tiles.names import ProtoTileNames
from tileset import SquareTileSet


class Zelda2ProtoTileNames(ProtoTileNames):
    LOWER = auto()
    UPPER = auto()
    WALL = auto()
    WALL_CORNER = auto()
    STAIRS = auto()
    WALL_BRIDGE = auto()
    FLOOR_BRIDGE = auto()
    BRIDGE_CORNER = auto()
    BRIDGE_CORNER_COLUMN = auto()


def generate_tile_pixels():
    img = plt.imread('assets/zelda-like-3.png')
    arr = img[:, :, 0]
    s = 16

    def end_tile(i):
        return i + s - 1

    def extract_tile(i, j):
        return arr[i:end_tile(i), j:end_tile(j)]

    return {
        name: TilePixels(extract_tile(s * i, s * j)) for name, (i, j) in {
            Zelda2ProtoTileNames.UPPER: (0, 0),
            Zelda2ProtoTileNames.LOWER: (2, 2),
            Zelda2ProtoTileNames.WALL_CORNER: (0, 1),
            Zelda2ProtoTileNames.STAIRS: (0, 2),
            Zelda2ProtoTileNames.WALL: (1, 0),
            Zelda2ProtoTileNames.WALL_BRIDGE: (1, 1),
            Zelda2ProtoTileNames.FLOOR_BRIDGE: (1, 2),
            Zelda2ProtoTileNames.BRIDGE_CORNER_COLUMN: (2, 0),
            Zelda2ProtoTileNames.BRIDGE_CORNER: (2, 1),
        }.items()
    }


class Zelda2TileSet(SquareTileSet):
    SYM_PROTO_TILE_NAMES_ENUM_NAME = "SymZelda2ProtoTileNames"
    proto_tile_name_enum = Zelda2ProtoTileNames
    proto_connector_enum = Zelda2ProtoConnectors

    def get_symmetry_generators(self):
        return self.symmetry_generators_from_constraints()

    @property
    def connector_symmetries(self) -> Dict[ProtoConnectors, Group]:
        hz_stab = GeneratedGroup({Group.flip_x(), Group.flip_y()})
        return {
            self.proto_connector_enum.UPPER: None,
            self.proto_connector_enum.LOWER: None,
            self.proto_connector_enum.WALL: GeneratedGroup({Group.flip_y()}),
            self.proto_connector_enum.BRIDGE: hz_stab,
        }

    @property
    def tile_symmetries(self) -> Dict[ProtoTileNames, Group]:
        return {}

    @property
    def tile_constraints(self) -> Dict[ProtoTileNames, TileConstraints]:
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        lower = connector_dict[self.proto_connector_enum.LOWER]
        upper = connector_dict[self.proto_connector_enum.UPPER]
        wall_hz = connector_dict[self.proto_connector_enum.WALL]
        wall_vt = wall_hz.transform(Group.rot90())
        bridge_hz = connector_dict[self.proto_connector_enum.BRIDGE]
        bridge_vt = bridge_hz.transform(Group.rot90())

        return {
            self.proto_tile_name_enum.LOWER: TileConstraints.make_constraints_2d(
                up=lower,
                down=lower,
                left=lower,
                right=lower,
            ),
            self.proto_tile_name_enum.UPPER: TileConstraints.make_constraints_2d(
                up=upper,
                down=upper,
                left=upper,
                right=upper,
            ),
            self.proto_tile_name_enum.WALL: TileConstraints.make_constraints_2d(
                up=upper,
                down=lower,
                left=wall_hz,
                right=wall_hz,
            ),
            self.proto_tile_name_enum.WALL_CORNER: TileConstraints.make_constraints_2d(
                up=wall_vt,
                down=lower,
                left=wall_hz,
                right=lower,
            ),
            self.proto_tile_name_enum.STAIRS: TileConstraints.make_constraints_2d(
                up=upper,
                down=lower,
                left=wall_hz,
                right=wall_hz,
            ),
            self.proto_tile_name_enum.WALL_BRIDGE: TileConstraints.make_constraints_2d(
                up=upper,
                down=bridge_vt,
                left=wall_hz,
                right=wall_hz,
            ),
            self.proto_tile_name_enum.FLOOR_BRIDGE: TileConstraints.make_constraints_2d(
                up=bridge_vt,
                down=bridge_vt,
                left=lower,
                right=lower,
            ),
            self.proto_tile_name_enum.BRIDGE_CORNER: TileConstraints.make_constraints_2d(
                up=lower,
                down=bridge_vt,
                left=lower,
                right=bridge_hz,
            ),
            self.proto_tile_name_enum.BRIDGE_CORNER_COLUMN: TileConstraints.make_constraints_2d(
                up=bridge_vt,
                down=lower,
                left=lower,
                right=bridge_hz,
            ),
        }

    @property
    def tile_weights(self) -> Dict[ProtoTileNames, float]:
        return {
            self.proto_tile_name_enum.UPPER: 20,
            self.proto_tile_name_enum.LOWER: 20,
            self.proto_tile_name_enum.WALL: 5,
            self.proto_tile_name_enum.WALL_CORNER: 2,
            self.proto_tile_name_enum.STAIRS: 1,
            self.proto_tile_name_enum.WALL_BRIDGE: 1,
            self.proto_tile_name_enum.FLOOR_BRIDGE: 1,
            self.proto_tile_name_enum.BRIDGE_CORNER: 0.001,
            self.proto_tile_name_enum.BRIDGE_CORNER_COLUMN: 0.001,
        }

    @property
    def tile_graphics(self) -> Dict[ProtoTileNames, TilePixels]:
        return generate_tile_pixels()

    def __init__(self):
        super().__init__()
