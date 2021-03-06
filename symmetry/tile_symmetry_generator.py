from __future__ import annotations
from enum import Enum
from typing import Dict, Optional

from symmetry.coset import GroupCoset
from symmetry.groups import GroupAction, Group, GroupTargetMixin
from tiles.data import TileConstraints, ProtoTileData
from tiles.names import ProtoTileNames


class TileSymmetryGenerator:
    def __init__(self, action_dict: Dict[GroupAction, GroupTargetMixin]):
        self.action_dict = action_dict

    @classmethod
    def from_symmetries(cls, symmetry: Optional[Group], tile_transformation_group: Group) -> TileSymmetryGenerator:
        if symmetry is None:
            symmetry = tile_transformation_group
        return TileSymmetryGenerator(GroupCoset.partition_group_dict(tile_transformation_group, symmetry))

    @classmethod
    def from_constraint_symmetries(cls, constraints: TileConstraints, tile_transformation_group: Group):
        return TileSymmetryGenerator(constraints.generate_from_group(tile_transformation_group))

    def _transform_tile(self, name_enum: ProtoTileNames, g_action: GroupAction, tile_data: ProtoTileData):
        return ProtoTileData(
            name=name_enum(self.transform_tile_name(g_action, tile_data.name)),
            weight=tile_data.weight,  # todo consider dividing by # generated tiles?
            constraints=tile_data.constraints.transform(g_action),
            graphics=tile_data.graphics.transform(g_action)
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
        return self.action_dict.keys()
