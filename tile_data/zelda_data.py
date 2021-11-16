from enum import auto

from matplotlib import pyplot as plt

from directions import Directions
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Trivial, Group, Z4_SQUARE, GeneratedGroup
from tile_data.connectors import ZeldaProtoConnectors
from tiles import ProtoTileNames, TilePixels
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
    z2_swap = GeneratedGroup({Group.swap_xy()})
    z2_y = GeneratedGroup({Group.flip_y()})
    tile_symmetries = {
        proto_tile_name_enum.FLOOR: Trivial(),
        proto_tile_name_enum.WALL: z2_swap,
        proto_tile_name_enum.WALL_CORNER: Z4_SQUARE,
        proto_tile_name_enum.STAIRS: z2_swap,
        proto_tile_name_enum.WALL_BRIDGE: Z4_SQUARE,
        proto_tile_name_enum.FLOOR_BRIDGE: z2_swap,
        proto_tile_name_enum.BRIDGE_CORNER_COLUMN: z2_y,
        proto_tile_name_enum.BRIDGE_CORNER: z2_y,
    }
    hz_stab = GeneratedGroup({Group.flip_x(), Group.flip_y()})
    connector_symmetries = {
        proto_connector_enum.NONE: None,
        proto_connector_enum.WALL: hz_stab,
        proto_connector_enum.BRIDGE: hz_stab
    }
    connector_dict = ConnectorSymmetryGenerator(connector_symmetries).make_base_connector_dict()
    none = connector_dict[proto_connector_enum.NONE]
    wall_hz = connector_dict[proto_connector_enum.WALL]
    wall_vt = wall_hz.transform(Group.rot90())
    bridge_hz = connector_dict[proto_connector_enum.BRIDGE]
    bridge_vt = bridge_hz.transform(Group.rot90())

    tile_constraints = {
        proto_tile_name_enum.FLOOR: {
            Directions.UP: none,
            Directions.DOWN: none,
            Directions.LEFT: none,
            Directions.RIGHT: none,
        },
        proto_tile_name_enum.WALL: {
            Directions.UP: none,
            Directions.DOWN: none,
            Directions.LEFT: wall_hz,
            Directions.RIGHT: wall_hz,
        },
        proto_tile_name_enum.WALL_CORNER: {
            Directions.UP: wall_vt,
            Directions.DOWN: none,
            Directions.LEFT: wall_hz,
            Directions.RIGHT: none,
        },
        proto_tile_name_enum.STAIRS: {
            Directions.UP: none,
            Directions.DOWN: none,
            Directions.LEFT: wall_hz,
            Directions.RIGHT: wall_hz,
        },
        proto_tile_name_enum.WALL_BRIDGE: {
            Directions.UP: none,
            Directions.DOWN: bridge_vt,
            Directions.LEFT: wall_hz,
            Directions.RIGHT: wall_hz,
        },
        proto_tile_name_enum.FLOOR_BRIDGE: {
            Directions.UP: bridge_vt,
            Directions.DOWN: bridge_vt,
            Directions.LEFT: none,
            Directions.RIGHT: none,
        },
        proto_tile_name_enum.BRIDGE_CORNER: {
            Directions.UP: none,
            Directions.DOWN: bridge_vt,
            Directions.LEFT: none,
            Directions.RIGHT: bridge_hz,
        },
        proto_tile_name_enum.BRIDGE_CORNER_COLUMN: {
            Directions.UP: bridge_vt,
            Directions.DOWN: none,
            Directions.LEFT: none,
            Directions.RIGHT: bridge_hz,
        },
    }
    tile_weights = {
        proto_tile_name_enum.FLOOR: 20,
        proto_tile_name_enum.WALL: 5,
        proto_tile_name_enum.WALL_CORNER: 2,
        proto_tile_name_enum.STAIRS: 1,
        proto_tile_name_enum.WALL_BRIDGE: 1,
        proto_tile_name_enum.FLOOR_BRIDGE: 1,
        proto_tile_name_enum.BRIDGE_CORNER: 0.0,
        proto_tile_name_enum.BRIDGE_CORNER_COLUMN: 0.0,

    }
    tile_imgs = generate_tile_pixels()

    def __init__(self):
        super().__init__()
