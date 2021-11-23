from enum import Enum, auto

from abc_enum import ABCEnumMeta
from connectors import ProtoConnectors
from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.cubic_groups import CubicGroupAction, D4_SQUARE_Z
from symmetry.groups import GeneratedGroup, Group
from tiles.data import TileConstraints
from tiles.names import ProtoTileNames
from tileset import CubicTileSet, TileSet


class BuildingProtoTileNames(ProtoTileNames):
    EMPTY = ' '
    SOLID = '#'
    FLOOR = '_'
    WALL_EDGE = 'e'
    WALL_INNER_CORNER = 'c'
    WALL_OUTER_CORNER = 'C'
    DOORWAY = 'd'


class BuildingProtoConnectors(ProtoConnectors, Enum, metaclass=ABCEnumMeta):
    EMPTY = auto()
    SOLID = auto()
    DOORWAY = auto()
    ABOVE_FLOOR = auto()
    FLOOR_AND_WALL_X = auto()


_diaxial_symmetry = GeneratedGroup({CubicGroupAction.xy90(), CubicGroupAction.flip_z(), CubicGroupAction.flip_x()})


class BuildingTileSet(CubicTileSet):

    SYM_PROTO_TILE_NAMES_ENUM_NAME = "BuildingProtoTileNames"
    proto_tile_name_enum = BuildingProtoTileNames
    proto_connector_enum = BuildingProtoConnectors

    @property
    def tile_transformation_group(self) -> Group:
        return D4_SQUARE_Z

    @property
    def tile_symmetries(self):
        return {}

    def get_symmetry_generators(self):
        return self.symmetry_generators_from_constraints()

    @property
    def connector_symmetries(self):
        return {
            self.proto_connector_enum.EMPTY: None,
            self.proto_connector_enum.SOLID: None,
            self.proto_connector_enum.DOORWAY: None,
            self.proto_connector_enum.ABOVE_FLOOR: None,
            self.proto_connector_enum.FLOOR_AND_WALL_X: GeneratedGroup({CubicGroupAction.flip_y()})
        }

    @property
    def tile_constraints(self):
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        empty, solid, doorway, above_floor = [
            connector_dict[pc] for pc in (
                self.proto_connector_enum.EMPTY, self.proto_connector_enum.SOLID,
                self.proto_connector_enum.DOORWAY, self.proto_connector_enum.ABOVE_FLOOR
            )
        ]
        fw_right = connector_dict[self.proto_connector_enum.FLOOR_AND_WALL_X]
        fw_left = fw_right.transform(CubicGroupAction.flip_x())
        fw_out = fw_right.transform(CubicGroupAction.xy90())
        fw_in = fw_out.transform(CubicGroupAction.flip_y())
        return {
            self.proto_tile_name_enum.EMPTY: TileConstraints.make_constraints_3d(
                *(empty for _ in range(6))
            ),
            self.proto_tile_name_enum.SOLID: TileConstraints.make_constraints_3d(
                *(solid for _ in range(6))
            ),
            self.proto_tile_name_enum.FLOOR: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=above_floor, right=above_floor,
                in_=above_floor, out=above_floor
            ),
            self.proto_tile_name_enum.WALL_EDGE: TileConstraints.make_constraints_3d(
                up=empty, down=solid,  # this needs to change since wall does not terminate
                left=fw_out, right=fw_out,
                in_=above_floor, out=solid
            ),
            self.proto_tile_name_enum.WALL_INNER_CORNER: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=fw_out, right=solid,
                in_=fw_right, out=solid
            ),
            self.proto_tile_name_enum.WALL_OUTER_CORNER: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=above_floor, right=fw_out,
                in_=above_floor, out=fw_right
            ),
            self.proto_tile_name_enum.DOORWAY: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=fw_out, right=fw_out,
                in_=above_floor, out=doorway
            ),

        }

    @property
    def tile_weights(self):
        return {
            self.proto_tile_name_enum.EMPTY: 3,
            self.proto_tile_name_enum.SOLID: 3,
            self.proto_tile_name_enum.FLOOR: 3,
            self.proto_tile_name_enum.WALL_EDGE: 3,
            self.proto_tile_name_enum.WALL_INNER_CORNER: 1,
            self.proto_tile_name_enum.WALL_OUTER_CORNER: 1,
            self.proto_tile_name_enum.DOORWAY: 0.1
        }

    def __init__(self):
        super().__init__()
