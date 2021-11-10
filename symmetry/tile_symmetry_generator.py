from enum import Enum
from typing import Dict

from connectors import Connectors
from directions import Directions
from symmetry.groups import GroupAction, Group
from tiles import ProtoTileNames, ProtoTileData


class TileSymmetryGenerator:
    def __init__(self, symmetry: Group):
        self.symmetry = symmetry

    @staticmethod
    def _transform_constraints(g_action: GroupAction, constraints: Dict[Directions, Connectors]) -> Dict[
        Directions, Connectors]:
        return {
            g_action.transform(direction): g_action.transform(connector)
            for direction, connector in constraints.items()
        }

    def _transform_tile(self, name_enum: ProtoTileNames, g_action: GroupAction, tile_data: ProtoTileData):
        return ProtoTileData(
            name=name_enum(self.transform_tile_name(g_action, tile_data.name)),
            weight=tile_data.weight,  # todo consider dividing by # group elements?
            constraints=self._transform_constraints(g_action, tile_data.constraints),
            pixels=g_action.transform(tile_data.pixels)
        )

    @staticmethod
    def transform_tile_name(g_action: GroupAction, proto_tile_name: Enum) -> str:
        return f"{proto_tile_name.value}_{g_action.name}"

    def generate(self, name_enum: ProtoTileNames, tile_data: ProtoTileData):
        return {
            tile_data.name: tile_data
            for tile_data in (
                self._transform_tile(name_enum, g, tile_data) for g in self.symmetry.get_elements()
            )
        }

    def generate_tile_names(self, tile_data: ProtoTileData):
        return {self.transform_tile_name(g, tile_data.name) for g in self.symmetry.get_elements()}