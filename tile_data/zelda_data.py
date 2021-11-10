from enum import auto

from matplotlib import pyplot as plt

from directions import Directions
from symmetry.groups import Trivial, Group, Z4, Z2
from tile_data.connectors import ZeldaConnectors
from tiles import ProtoTileNames
from tileset import TileSet

ConnectorsEnum = ZeldaConnectors

class ZeldaProtoTileNames(ProtoTileNames):
    FLOOR = auto()
    WALL = auto()
    WALL_CORNER = auto()
    STAIRS = auto()
    WALL_BRIDGE = auto()
    FLOOR_BRIDGE = auto()
    BRIDGE_CORNER =auto()
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
        name: extract_tile(s * i, s * j) for name, (i, j) in {
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
    z4_rot = Z4(Group.rot90())
    z2_swap = Z2(Group.swap_xy())
    z2_y = Z2(Group.flip_y())
    tile_symmetries = {
        proto_tile_name_enum.FLOOR: Trivial(),
        proto_tile_name_enum.WALL: z2_swap,
        proto_tile_name_enum.WALL_CORNER: z4_rot,
        proto_tile_name_enum.STAIRS: z2_swap,
        proto_tile_name_enum.WALL_BRIDGE: z4_rot,
        proto_tile_name_enum.FLOOR_BRIDGE: z2_swap,
        proto_tile_name_enum.BRIDGE_CORNER_COLUMN: z2_y,
        proto_tile_name_enum.BRIDGE_CORNER: z2_y,
    }
    tile_constraints = {
        proto_tile_name_enum.FLOOR: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.NONE,
        },
        proto_tile_name_enum.WALL: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.WALL_HORIZONTAL,
            Directions.RIGHT: ConnectorsEnum.WALL_HORIZONTAL,
        },
        proto_tile_name_enum.WALL_CORNER: {
            Directions.UP: ConnectorsEnum.WALL_VERTICAL,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.WALL_HORIZONTAL,
            Directions.RIGHT: ConnectorsEnum.NONE,
        },
        proto_tile_name_enum.STAIRS: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.WALL_HORIZONTAL,
            Directions.RIGHT: ConnectorsEnum.WALL_HORIZONTAL,
        },
        proto_tile_name_enum.WALL_BRIDGE: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.BRIDGE_VERTICAL,
            Directions.LEFT: ConnectorsEnum.WALL_HORIZONTAL,
            Directions.RIGHT: ConnectorsEnum.WALL_HORIZONTAL,
        },
        proto_tile_name_enum.FLOOR_BRIDGE: {
            Directions.UP: ConnectorsEnum.BRIDGE_VERTICAL,
            Directions.DOWN: ConnectorsEnum.BRIDGE_VERTICAL,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.NONE,
        },
        proto_tile_name_enum.BRIDGE_CORNER: {
            Directions.UP: ConnectorsEnum.NONE,
            Directions.DOWN: ConnectorsEnum.BRIDGE_VERTICAL,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.BRIDGE_HORIZONTAL,
        },
        proto_tile_name_enum.BRIDGE_CORNER_COLUMN: {
            Directions.UP: ConnectorsEnum.BRIDGE_VERTICAL,
            Directions.DOWN: ConnectorsEnum.NONE,
            Directions.LEFT: ConnectorsEnum.NONE,
            Directions.RIGHT: ConnectorsEnum.BRIDGE_HORIZONTAL,
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

