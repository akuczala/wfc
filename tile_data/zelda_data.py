from enum import auto
from typing import Dict

from matplotlib import pyplot as plt

from connectors import ProtoConnectors
from directions import Directions
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Trivial, Group, GeneratedGroup
from tile_data.connectors import ZeldaProtoConnectors
from tiles import ProtoTileNames, TilePixels, TileConstraints
from tileset import TileSet


class ZeldaProtoTileNames(ProtoTileNames):
    FLOOR = auto()
    WALL = auto()
    WALL_CORNER = auto()
    STAIRS = auto()
    WALL_BRIDGE = auto()
    FLOOR_BRIDGE = auto()
    BRIDGE_CORNER = auto()
    BRIDGE_CORNER_COLUMN = auto()


def generate_tile_pixels():
    img = plt.imread('assets/zelda-like-2.png')
    arr = img[:, :, 0]
    s = 16

    def end_tile(i):
        return i + s - 1

    def extract_tile(i, j):
        return arr[i:end_tile(i), j:end_tile(j)]

    return {
        name: TilePixels(extract_tile(s * i, s * j)) for name, (i, j) in {
            ZeldaProtoTileNames.FLOOR: (0, 0),
            ZeldaProtoTileNames.WALL_CORNER: (0, 1),
            ZeldaProtoTileNames.STAIRS: (0, 2),
            ZeldaProtoTileNames.WALL: (1, 0),
            ZeldaProtoTileNames.WALL_BRIDGE: (1, 1),
            ZeldaProtoTileNames.FLOOR_BRIDGE: (1, 2),
            ZeldaProtoTileNames.BRIDGE_CORNER_COLUMN: (2, 0),
            ZeldaProtoTileNames.BRIDGE_CORNER: (2, 1),
        }.items()
    }


class ZeldaTileSet(TileSet):
    SYM_PROTO_TILE_NAMES_ENUM_NAME = "SymZeldaProtoTileNames"
    proto_tile_name_enum = ZeldaProtoTileNames
    proto_connector_enum = ZeldaProtoConnectors

    def get_symmetry_generators(self):
        return self.symmetry_generators_from_constraints()

    @property
    def connector_symmetries(self) -> Dict[ProtoConnectors, Group]:
        hz_stab = GeneratedGroup({Group.flip_x(), Group.flip_y()})
        return {
            self.proto_connector_enum.NONE: None,
            self.proto_connector_enum.WALL: hz_stab,
            self.proto_connector_enum.BRIDGE: hz_stab
        }

    @property
    def tile_constraints(self) -> Dict[ProtoTileNames, TileConstraints]:
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        none = connector_dict[self.proto_connector_enum.NONE]
        wall_hz = connector_dict[self.proto_connector_enum.WALL]
        wall_vt = wall_hz.transform(Group.rot90())
        bridge_hz = connector_dict[self.proto_connector_enum.BRIDGE]
        bridge_vt = bridge_hz.transform(Group.rot90())

        return {
            self.proto_tile_name_enum.FLOOR: TileConstraints.make_constraints_2d(
                up=none,
                down=none,
                left=none,
                right=none,
            ),
            self.proto_tile_name_enum.WALL: TileConstraints.make_constraints_2d(
                up=none,
                down=none,
                left=wall_hz,
                right=wall_hz,
            ),
            self.proto_tile_name_enum.WALL_CORNER: TileConstraints.make_constraints_2d(
                up=wall_vt,
                down=none,
                left=wall_hz,
                right=none,
            ),
            self.proto_tile_name_enum.STAIRS: TileConstraints.make_constraints_2d(
                up=none,
                down=none,
                left=wall_hz,
                right=wall_hz,
            ),
            self.proto_tile_name_enum.WALL_BRIDGE: TileConstraints.make_constraints_2d(
                up=none,
                down=bridge_vt,
                left=wall_hz,
                right=wall_hz,
            ),
            self.proto_tile_name_enum.FLOOR_BRIDGE: TileConstraints.make_constraints_2d(
                up=bridge_vt,
                down=bridge_vt,
                left=none,
                right=none,
            ),
            self.proto_tile_name_enum.BRIDGE_CORNER: TileConstraints.make_constraints_2d(
                up=none,
                down=bridge_vt,
                left=none,
                right=bridge_hz,
            ),
            self.proto_tile_name_enum.BRIDGE_CORNER_COLUMN: TileConstraints.make_constraints_2d(
                up=bridge_vt,
                down=none,
                left=none,
                right=bridge_hz,
            ),
        }

    @property
    def tile_weights(self) -> Dict[ProtoTileNames, float]:
        return {
            self.proto_tile_name_enum.FLOOR: 20,
            self.proto_tile_name_enum.WALL: 5,
            self.proto_tile_name_enum.WALL_CORNER: 2,
            self.proto_tile_name_enum.STAIRS: 1,
            self.proto_tile_name_enum.WALL_BRIDGE: 1,
            self.proto_tile_name_enum.FLOOR_BRIDGE: 1,
            self.proto_tile_name_enum.BRIDGE_CORNER: 0.0,
            self.proto_tile_name_enum.BRIDGE_CORNER_COLUMN: 0.0,

        }

    @property
    def tile_imgs(self) -> Dict[ProtoTileNames, TilePixels]:
        return generate_tile_pixels()

    def __init__(self):
        super().__init__()
