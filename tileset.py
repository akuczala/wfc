from abc import ABC
from enum import Enum
from typing import Dict, Type, Set

import numpy as np

from connectors import Connectors
from directions import Directions
from symmetry import TileSymmetryGenerator, Group, GroupAction
from tiles import ProtoTileData, ProtoTileNames, TileData, TileNames


class TileSet(ABC):
    SYM_PROTO_TILE_NAMES_ENUM_NAME: str
    proto_tile_name_enum: Type[ProtoTileNames]
    tile_constraints: Dict[ProtoTileNames, Dict[Directions, Connectors]]
    tile_weights: Dict[ProtoTileNames, float]
    tile_imgs: Dict[ProtoTileNames, np.ndarray]
    tile_symmetries: Dict[ProtoTileNames, Group]

    def __init__(self):
        self.proto_tile_data = self.build_proto_data()
        self.sym_proto_tile_data = self.symmetry_build()
        self.tile_data = self.generate_compatible_tiles()
        self.tile_name_enum: Type[ProtoTileNames]

    @classmethod
    def build_proto_data(cls) -> Dict[ProtoTileNames, ProtoTileData]:
        return {
            name: ProtoTileData(
                name=name,
                constraints=cls.tile_constraints[name],
                weight=cls.tile_weights[name],
                pixels=cls.tile_imgs[name]
            )
            for name in cls.proto_tile_name_enum
        }

    def generate_compatible_tiles(self):
        return {
            tile: TileData(
                name=tile,
                weight=self.sym_proto_tile_data[tile].weight,
                compatible_tiles={
                    direction: self.get_constraint_compatible_tiles(tile, direction)
                    for direction in Directions
                },
                pixels=self.sym_proto_tile_data[tile].pixels
            ) for tile in self.tile_name_enum
        }

    def get_constraint_compatible_tiles(self, this_tile: ProtoTileNames, direction: Directions):
        connector = self.sym_proto_tile_data[this_tile].constraints[direction]
        return {
            tile for tile in self.tile_name_enum
            if self.sym_proto_tile_data[tile].constraints[direction.reverse()] == connector
        }

    def symmetry_build(self):
        new_tile_names = set()
        sym_gens = {name: TileSymmetryGenerator(self.tile_symmetries[name]) for name in self.proto_tile_name_enum}
        for name in sym_gens.keys():
            new_tile_names = new_tile_names.union(sym_gens[name].generate_tile_names(self.proto_tile_data[name]))
        self.tile_name_enum = Enum(self.SYM_PROTO_TILE_NAMES_ENUM_NAME, {name: name for name in new_tile_names})
        output_tiles = {}
        for name, tile_data in self.proto_tile_data.items():
            output_tiles.update(sym_gens[name].generate(self.tile_name_enum, tile_data))
        return output_tiles

    def get_tile_name(self, proto_tile_name: ProtoTileNames, g: GroupAction) -> TileNames:
        return self.tile_name_enum(
            TileSymmetryGenerator.transform_tile_name(g, proto_tile_name)
        )

    def get_tile_names(self, proto_tile_name: ProtoTileNames) -> Set[TileNames]:
        return {
            self.get_tile_name(proto_tile_name, g)
            for g in self.tile_symmetries[proto_tile_name].get_elements()
        }