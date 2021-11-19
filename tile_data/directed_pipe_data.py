from typing import Dict

from matplotlib import pyplot as plt

from connectors import ProtoConnectors
from directions import Directions
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.groups import Trivial, Z4_SQUARE, D4_SQUARE, GeneratedGroup, Group
from tile_data.connectors import DirectedPipeProtoConnectors
from tiles import ProtoTileNames, TilePixels, TileConstraints
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

    @property
    def tile_weights(self) -> Dict[ProtoTileNames, float]:
        return {
            self.proto_tile_name_enum.EMPTY: 100,
            self.proto_tile_name_enum.PIPE: 3,
            self.proto_tile_name_enum.CROSS_PIPE: 0.1,
            self.proto_tile_name_enum.ANGLE_PIPE: 0.5,
            self.proto_tile_name_enum.EMITTER: 0.0,
            self.proto_tile_name_enum.CONSUMER: 0.0,
            self.proto_tile_name_enum.SPLITTER: 0.001,
            self.proto_tile_name_enum.MERGER: 0.001,
        }

    @property
    def tile_imgs(self) -> Dict[ProtoTileNames, TilePixels]:
        return generate_tile_pixels()

    @property
    def tile_symmetries(self) -> Dict[ProtoTileNames, Group]:
        return {
            # self.proto_tile_name_enum.EMPTY: None,
            # self.proto_tile_name_enum.PIPE: GeneratedGroup({Group.flip_x()}),
            # self.proto_tile_name_enum.CROSS_PIPE: GeneratedGroup({Group.swap_xy()}),
            # self.proto_tile_name_enum.ANGLE_PIPE: Trivial(),
            # self.proto_tile_name_enum.EMITTER: GeneratedGroup({Group.flip_y()}),
            # self.proto_tile_name_enum.CONSUMER: GeneratedGroup({Group.flip_y()}),
            # self.proto_tile_name_enum.SPLITTER: Trivial(),
            # self.proto_tile_name_enum.MERGER: Trivial(),
        }

    def get_symmetry_generators(self):
        return self.symmetry_generators_from_constraints()

    @property
    def connector_symmetries(self) -> Dict[ProtoConnectors, Group]:
        return {
            self.proto_connector_enum.NONE: None,
            self.proto_connector_enum.UP: GeneratedGroup({Group.flip_y()})
        }

    @property
    def tile_constraints(self) -> Dict[ProtoTileNames, TileConstraints]:
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        none = connector_dict[self.proto_connector_enum.NONE]
        up = connector_dict[self.proto_connector_enum.UP]
        left = up.transform(Group.rot90())
        down = left.transform(Group.rot90())
        right = down.transform(Group.rot90())
        return {
            self.proto_tile_name_enum.EMPTY: TileConstraints.make_constraints(
                up=none,
                down=none,
                left=none,
                right=none,
            ),
            self.proto_tile_name_enum.PIPE: TileConstraints.make_constraints(
                up=none,
                down=none,
                left=right,
                right=right,
            ),
            self.proto_tile_name_enum.CROSS_PIPE: TileConstraints.make_constraints(
                up=up,
                down=up,
                left=right,
                right=right,
            ),
            self.proto_tile_name_enum.ANGLE_PIPE: TileConstraints.make_constraints(
                up=up,
                down=none,
                left=none,
                right=left,
            ),
            self.proto_tile_name_enum.EMITTER: TileConstraints.make_constraints(
                up=up,
                down=none,
                left=none,
                right=none,
            ),
            self.proto_tile_name_enum.CONSUMER: TileConstraints.make_constraints(
                up=down,
                down=none,
                left=none,
                right=none,
            ),
            self.proto_tile_name_enum.SPLITTER: TileConstraints.make_constraints(
                up=none,
                down=down,
                left=right,
                right=right,
            ),
            self.proto_tile_name_enum.MERGER: TileConstraints.make_constraints(
                up=none,
                down=down,
                left=right,
                right=left,
            )
        }

    def __init__(self):
        super().__init__()
