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

    RAILING_EDGE = 'r'
    RAILING_INNER_CORNER = 'p'
    RAILING_OUTER_CORNER = 'P'
    RAILING_DOORWAY = 'D'

    RAILING_FLOOR_EDGE = 'f'
    RAILING_FLOOR_INNER_CORNER = 'q'
    RAILING_FLOOR_OUTER_CORNER = 'Q'
    RAILING_FLOOR_DOORWAY = '∂'

    STAIR_BOTTOM = 'b'  # replace with DOORWAY?
    STAIR_TOP = 't'  # replace with RAILING_FLOOR_DOORWAY?
    STAIR_EMBEDDED = 's'


class BuildingProtoConnectors(ProtoConnectors, Enum, metaclass=ABCEnumMeta):
    EMPTY = auto()
    SOLID = auto()
    DOORWAY = auto()
    ABOVE_FLOOR = auto()
    FLOOR_AND_WALL_X = auto()

    RAILING_X = auto()
    RAILING_AND_FLOOR_X = auto()
    RAILING_INSIDE = auto()

    RAILING_WALL_EDGE_X = auto()
    RAILING_WALL_INNER_CORNER = auto()
    RAILING_WALL_OUTER_CORNER = auto()
    RAILING_WALL_DOORWAY = auto()

    RAILING_DOORWAY = auto()
    RAILING_FLOOR_DOORWAY = auto()

    STAIR_TOP = auto()
    STAIR_BOTTOM = auto()


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
        pcm = self.proto_connector_enum
        along_x = GeneratedGroup({CubicGroupAction.flip_y()})
        along_y = GeneratedGroup({CubicGroupAction.flip_x()})
        corner_sym = GeneratedGroup({CubicGroupAction.swap_xy()})
        return {
            pcm.EMPTY: None,
            pcm.SOLID: None,
            pcm.DOORWAY: None,
            pcm.ABOVE_FLOOR: None,
            pcm.FLOOR_AND_WALL_X: along_x,
            pcm.RAILING_X: along_x,
            pcm.RAILING_AND_FLOOR_X: along_x,
            pcm.RAILING_INSIDE: along_x,
            pcm.RAILING_WALL_EDGE_X: along_x,
            pcm.RAILING_WALL_INNER_CORNER: corner_sym,
            pcm.RAILING_WALL_OUTER_CORNER: corner_sym,
            pcm.RAILING_DOORWAY: along_y,
            pcm.RAILING_WALL_DOORWAY: None,
            pcm.RAILING_FLOOR_DOORWAY: None,

            pcm.STAIR_TOP: along_y,
            pcm.STAIR_BOTTOM: None,
        }

    # def _edge_template(self, pointing_connector, up, down) -> TileConstraints:
    #     c_out = pointing_connector.transform(CubicGroupAction.xy90())
    #     return TileConstraints.make_constraints_3d(
    #             up=rw_out, down=solid,
    #             left=c_out, right=c_out,
    #             in_=above_floor, out=solid
    #         ),

    @property
    def tile_constraints(self):
        pcm = self.proto_connector_enum
        ptn = self.proto_tile_name_enum
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        empty, solid, doorway, above_floor = [
            connector_dict[pc] for pc in (
                pcm.EMPTY, pcm.SOLID,
                pcm.DOORWAY, pcm.ABOVE_FLOOR
            )
        ]
        fw_right = connector_dict[pcm.FLOOR_AND_WALL_X]
        fw_out = fw_right.transform(CubicGroupAction.xy90())

        r_right = connector_dict[pcm.RAILING_X]
        r_out = r_right.transform(CubicGroupAction.xy90())

        rw_right = connector_dict[pcm.RAILING_WALL_EDGE_X]
        rw_out = rw_right.transform(CubicGroupAction.xy90())

        rf_right = connector_dict[pcm.RAILING_AND_FLOOR_X]
        rf_out = rf_right.transform(CubicGroupAction.xy90())

        # point out of railings (from floor to empty)
        ri_right = connector_dict[pcm.RAILING_INSIDE]
        ri_left = ri_right.transform(CubicGroupAction.flip_x())
        ri_out = ri_right.transform(CubicGroupAction.xy90())
        ri_in = ri_out.transform(CubicGroupAction.flip_y())
        return {
            ptn.EMPTY: TileConstraints.make_constraints_3d(
                *(empty for _ in range(6))
            ),
            ptn.SOLID: TileConstraints.make_constraints_3d(
                *(solid for _ in range(6))
            ),
            ptn.FLOOR: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=above_floor, right=above_floor,
                in_=above_floor, out=above_floor
            ),
            ptn.WALL_EDGE: TileConstraints.make_constraints_3d(
                up=rw_out, down=solid,
                left=fw_out, right=fw_out,
                in_=above_floor, out=solid
            ),
            ptn.WALL_INNER_CORNER: TileConstraints.make_constraints_3d(
                up=connector_dict[pcm.RAILING_WALL_INNER_CORNER], down=solid,
                left=fw_out, right=solid,
                in_=fw_right, out=solid
            ),
            ptn.WALL_OUTER_CORNER: TileConstraints.make_constraints_3d(
                up=connector_dict[pcm.RAILING_WALL_OUTER_CORNER], down=solid,
                left=above_floor, right=fw_out,
                in_=above_floor, out=fw_right
            ),
            ptn.DOORWAY: TileConstraints.make_constraints_3d(
                up=connector_dict[pcm.RAILING_WALL_DOORWAY], down=solid,
                left=fw_out, right=fw_out,
                in_=above_floor, out=doorway
            ),
            ptn.RAILING_EDGE: TileConstraints.make_constraints_3d(
                up=empty, down=rw_out,
                left=r_out, right=r_out,
                in_=empty, out=ri_in
            ),
            ptn.RAILING_INNER_CORNER: TileConstraints.make_constraints_3d(
                up=empty, down=connector_dict[pcm.RAILING_WALL_INNER_CORNER],
                left=r_out, right=ri_left,
                in_=r_right, out=ri_in
            ),
            ptn.RAILING_OUTER_CORNER: TileConstraints.make_constraints_3d(
                up=empty, down=connector_dict[pcm.RAILING_WALL_OUTER_CORNER],
                left=empty, right=r_out,
                in_=empty, out=r_right
            ),
            ptn.RAILING_DOORWAY: TileConstraints.make_constraints_3d(
                up=empty, down=connector_dict[pcm.RAILING_WALL_DOORWAY],
                left=r_out, right=r_out,
                in_=empty, out=connector_dict[pcm.RAILING_DOORWAY]
            ),
            ptn.RAILING_FLOOR_EDGE: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=rf_out, right=rf_out,
                in_=above_floor, out=ri_out
            ),
            ptn.RAILING_FLOOR_INNER_CORNER: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=rf_out, right=ri_right,
                in_=rf_right, out=ri_out
            ),
            ptn.RAILING_FLOOR_OUTER_CORNER: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=above_floor, right=rf_out,
                in_=above_floor, out=rf_right
            ),
            ptn.RAILING_FLOOR_DOORWAY: TileConstraints.make_constraints_3d(
                up=empty, down=solid,
                left=rf_out, right=rf_out,
                in_=above_floor, out=connector_dict[pcm.STAIR_TOP].transform(CubicGroupAction.flip_y())
            ),
            ptn.STAIR_BOTTOM: TileConstraints.make_constraints_3d(
                up=connector_dict[pcm.RAILING_WALL_DOORWAY], down=solid,
                left=fw_out, right=fw_out,
                in_=above_floor, out=connector_dict[pcm.STAIR_BOTTOM]
            ),
            ptn.STAIR_EMBEDDED: TileConstraints.make_constraints_3d(
                up=connector_dict[pcm.STAIR_TOP], down=solid,
                left=solid, right=solid,
                in_=connector_dict[pcm.STAIR_BOTTOM], out=solid
            ),
            ptn.STAIR_TOP: TileConstraints.make_constraints_3d(
                up=empty, down=connector_dict[pcm.STAIR_TOP],
                left=ri_right, right=ri_left,
                in_=connector_dict[pcm.RAILING_DOORWAY],
                out=connector_dict[pcm.STAIR_TOP]
            )

        }

    @property
    def tile_weights(self):
        ptn = self.proto_tile_name_enum
        return {
            ptn.EMPTY: 0.01,
            ptn.SOLID: 3,
            ptn.FLOOR: 2,
            ptn.WALL_EDGE: 10,
            ptn.WALL_INNER_CORNER: 1,
            ptn.WALL_OUTER_CORNER: 0.5,
            ptn.DOORWAY: 0.1,
            ptn.RAILING_EDGE: 1,
            ptn.RAILING_INNER_CORNER: 1,
            ptn.RAILING_OUTER_CORNER: 0.5,
            ptn.RAILING_DOORWAY: 0.1,
            ptn.RAILING_FLOOR_EDGE: 1,
            ptn.RAILING_FLOOR_INNER_CORNER: 1,
            ptn.RAILING_FLOOR_OUTER_CORNER: 0.5,
            ptn.RAILING_FLOOR_DOORWAY: 1,
            ptn.STAIR_BOTTOM: 1,
            ptn.STAIR_TOP: 1,
            ptn.STAIR_EMBEDDED: 1
        }

    def __init__(self):
        super().__init__()
