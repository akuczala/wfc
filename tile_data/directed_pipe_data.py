from matplotlib import pyplot as plt

from directions import Directions
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Trivial, Z4_SQUARE, D4_SQUARE, GeneratedGroup, Group
from tile_data.connectors import DirectedPipeProtoConnectors
from tiles import ProtoTileNames, TilePixels
from tileset import TileSet


class DirectedProtoTileNames(ProtoTileNames):
    EMPTY = 'EMPTY'
    PIPE = 'PIPE'
    CROSS_PIPE = 'CROSS_PIPE'
    ANGLE_PIPE = 'ANGLE_PIPE'
    EMITTER = 'EMITTER'
    CONSUMER = 'CONSUMER'
    SPLITTER = 'SPLITTER'
    MERGER = 'MERGER'


def generate_tile_pixels():
    img = plt.imread('assets/directed_pipe_tiles.png')
    arr = img[:, :, 0]
    s = 16

    def end_tile(i):
        return i + s - 1

    def extract_tile(i, j):
        return arr[i:end_tile(i), j:end_tile(j)]

    return {
        name: TilePixels(extract_tile(s * i, s * j)) for name, (i, j) in {
            DirectedProtoTileNames.PIPE: (0, 0),
            DirectedProtoTileNames.ANGLE_PIPE: (0, 1),
            DirectedProtoTileNames.CROSS_PIPE: (0, 2),
            DirectedProtoTileNames.EMPTY: (0, 3),
            DirectedProtoTileNames.EMITTER: (1, 0),
            DirectedProtoTileNames.CONSUMER: (1, 1),
            DirectedProtoTileNames.SPLITTER: (2, 0),
            DirectedProtoTileNames.MERGER: (2, 1),
        }.items()
    }


class DirectedPipeTileSet(TileSet):
    SYM_PROTO_TILE_NAMES_ENUM_NAME = "SymDirectedProtoTileNames"
    proto_tile_name_enum = DirectedProtoTileNames
    proto_connector_enum = DirectedPipeProtoConnectors
    tile_symmetries = {
        proto_tile_name_enum.EMPTY: Trivial(),
        proto_tile_name_enum.PIPE: Z4_SQUARE,
        proto_tile_name_enum.CROSS_PIPE: Z4_SQUARE,
        proto_tile_name_enum.ANGLE_PIPE: D4_SQUARE,
        proto_tile_name_enum.EMITTER: Z4_SQUARE,
        proto_tile_name_enum.CONSUMER: Z4_SQUARE,
        proto_tile_name_enum.SPLITTER: D4_SQUARE,
        proto_tile_name_enum.MERGER: D4_SQUARE,
    }
    connector_symmetries = {
        proto_connector_enum.NONE: None,
        proto_connector_enum.UP: GeneratedGroup({GeneratedGroup.flip_y()})
    }
    connector_dict = ConnectorSymmetryGenerator(connector_symmetries).make_base_connector_dict()
    none = connector_dict[proto_connector_enum.NONE]
    up = connector_dict[proto_connector_enum.UP]
    left = up.transform(Group.rot90())
    down = left.transform(Group.rot90())
    right = down.transform(Group.rot90())
    tile_constraints = {
        proto_tile_name_enum.EMPTY: {
            Directions.UP: none,
            Directions.DOWN: none,
            Directions.LEFT: none,
            Directions.RIGHT: none,
        },
        proto_tile_name_enum.PIPE: {
            Directions.UP: none,
            Directions.DOWN: none,
            Directions.LEFT: right,
            Directions.RIGHT: right,
        },
        proto_tile_name_enum.CROSS_PIPE: {
            Directions.UP: up,
            Directions.DOWN: up,
            Directions.LEFT: right,
            Directions.RIGHT: right,
        },
        proto_tile_name_enum.ANGLE_PIPE: {
            Directions.UP: up,
            Directions.DOWN: none,
            Directions.LEFT: none,
            Directions.RIGHT: left,
        },
        proto_tile_name_enum.EMITTER: {
            Directions.UP: up,
            Directions.DOWN: none,
            Directions.LEFT: none,
            Directions.RIGHT: none,
        },
        proto_tile_name_enum.CONSUMER: {
            Directions.UP: down,
            Directions.DOWN: none,
            Directions.LEFT: none,
            Directions.RIGHT: none,
        },
        proto_tile_name_enum.SPLITTER: {
            Directions.UP: none,
            Directions.DOWN: down,
            Directions.LEFT: right,
            Directions.RIGHT: right,
        },
        proto_tile_name_enum.MERGER: {
            Directions.UP: none,
            Directions.DOWN: down,
            Directions.LEFT: right,
            Directions.RIGHT: left,
        }
    }
    tile_weights = {
        proto_tile_name_enum.EMPTY: 1000,
        proto_tile_name_enum.PIPE: 3,
        proto_tile_name_enum.CROSS_PIPE: 0.1,
        proto_tile_name_enum.ANGLE_PIPE: 0.5,
        proto_tile_name_enum.EMITTER: 0.0,
        proto_tile_name_enum.CONSUMER: 0.0,
        proto_tile_name_enum.SPLITTER: 0.001,
        proto_tile_name_enum.MERGER: 0.001,

    }
    tile_imgs = generate_tile_pixels()

    def __init__(self):
        super().__init__()
