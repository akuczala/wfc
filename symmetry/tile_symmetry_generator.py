from enum import Enum
from typing import Dict, Optional

from connectors import Connectors
from directions import Directions
from symmetry.coset import GroupCoset
from symmetry.groups import GroupAction, Group, D4_SQUARE
from tiles import ProtoTileNames, ProtoTileData

TILE_TRANSFORMATION_GROUP = D4_SQUARE


class TileSymmetryGenerator:
    def __init__(self, symmetry: Optional[Group]):
        if symmetry is None:
            symmetry = TILE_TRANSFORMATION_GROUP
        self.coset_dict = GroupCoset.partition_group_dict(TILE_TRANSFORMATION_GROUP, symmetry)

    def _transform_tile(self, name_enum: ProtoTileNames, g_action: GroupAction, tile_data: ProtoTileData):
        return ProtoTileData(
            name=name_enum(self.transform_tile_name(g_action, tile_data.name)),
            weight=tile_data.weight,  # todo consider dividing by # generated tiles?
            constraints=tile_data.constraints.transform(g_action),
            pixels=tile_data.pixels.transform(g_action)
        )

    @staticmethod
    def transform_tile_name(g_action: GroupAction, proto_tile_name: Enum) -> str:
        return f"{proto_tile_name.value}_{g_action.name}"

    def generate(self, name_enum: ProtoTileNames, proto_tile_data: ProtoTileData):
        return {
            tile_data.name: tile_data
            for tile_data in (
                self._transform_tile(name_enum, g, proto_tile_data) for g in self.transformations
            )
        }

    def generate_tile_names(self, tile_name: ProtoTileNames):
        return {self.transform_tile_name(g, tile_name) for g in self.transformations}

    @property
    def transformations(self):
        return self.coset_dict.keys()
