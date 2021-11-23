from symmetry.connector_symmetry_generator import ConnectorSymmetryGenerator
from symmetry.cubic_groups import CubicGroupAction
from symmetry.groups import GeneratedGroup
from tile_data.connectors import PipeProtoConnectors
from tiles.data import TileConstraints
from tiles.names import ProtoTileNames
from tileset import CubicTileSet


class PipeProtoTileNames(ProtoTileNames):
    EMPTY = ' '
    HORIZONTAL_PIPE = '-'
    CROSS_PIPE = '+'
    ANGLE_PIPE = 'a'
    TERMINAL = 't'


_diaxial_symmetry = GeneratedGroup({CubicGroupAction.xy90(), CubicGroupAction.flip_z(), CubicGroupAction.flip_x()})


class Pipe3DTileSet(CubicTileSet):
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
            self.proto_connector_enum.HORIZONTAL: _diaxial_symmetry
        }

    @property
    def tile_constraints(self):
        connector_dict = ConnectorSymmetryGenerator(self.connector_symmetries).make_base_connector_dict()
        no_con, z_con = connector_dict[self.proto_connector_enum.NONE], connector_dict[
            self.proto_connector_enum.HORIZONTAL]
        x_con = z_con.transform(CubicGroupAction.xz90())
        y_con = z_con.transform(CubicGroupAction.yz90())
        return {
            PipeProtoTileNames.EMPTY: TileConstraints.make_constraints_3d(
                *(no_con for _ in range(6))
            ),
            PipeProtoTileNames.HORIZONTAL_PIPE: TileConstraints.make_constraints_3d(
                up=z_con, down=z_con,
                left=no_con, right=no_con,
                in_=no_con, out=no_con
            ),
            PipeProtoTileNames.CROSS_PIPE: TileConstraints.make_constraints_3d(
                up=z_con, down=z_con,
                left=x_con, right=x_con,
                in_=y_con, out=y_con
            ),
            PipeProtoTileNames.ANGLE_PIPE: TileConstraints.make_constraints_3d(
                up=z_con, down=no_con,
                left=no_con, right=no_con,
                in_=z_con, out=y_con
            ),
            PipeProtoTileNames.TERMINAL: TileConstraints.make_constraints_3d(
                up=no_con, down=z_con,
                left=no_con, right=no_con,
                in_=no_con, out=no_con
            ),
        }

    @property
    def tile_weights(self):
        return {
            PipeProtoTileNames.EMPTY: 400,
            PipeProtoTileNames.HORIZONTAL_PIPE: 3,
            PipeProtoTileNames.CROSS_PIPE: 0.1,
            PipeProtoTileNames.ANGLE_PIPE: 1,
            PipeProtoTileNames.TERMINAL: 0.01,
        }

    def __init__(self):
        super().__init__()
