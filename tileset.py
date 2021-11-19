from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, Set

import numpy as np

from connectors import Connectors, ProtoConnectors
from directions import Directions
from symmetry.groups import Group, GroupAction
from symmetry.tile_symmetry_generator import TileSymmetryGenerator
from tiles import ProtoTileData, ProtoTileNames, TileData, TileNames, TilePixels, TileConstraints


class TileSet(ABC):
    SYM_PROTO_TILE_NAMES_ENUM_NAME: str
    proto_tile_name_enum: Type[ProtoTileNames]
    proto_connector_enum: Type[ProtoConnectors]

    def __init__(self):
        self.proto_tile_data = self.build_proto_data()
        self.sym_proto_tile_data = self.symmetry_build()
        self.tile_data = self.generate_compatible_tiles()
        self.tile_name_enum: Type[ProtoTileNames]

    @property
    @abstractmethod
    def tile_constraints(self) -> Dict[ProtoTileNames, TileConstraints]:
        pass

    @property
    @abstractmethod
    def tile_weights(self) -> Dict[ProtoTileNames, float]:
        pass

    @property
    @abstractmethod
    def tile_imgs(self) -> Dict[ProtoTileNames, TilePixels]:
        pass

    @property
    @abstractmethod
    def tile_symmetries(self) -> Dict[ProtoTileNames, Group]:
        pass

    @property
    @abstractmethod
    def connector_symmetries(self) -> Dict[ProtoConnectors, Group]:
        pass

    def build_proto_data(self) -> Dict[ProtoTileNames, ProtoTileData]:
        return {
            name: ProtoTileData(
                name=name,
                constraints=self.tile_constraints[name],
                weight=self.tile_weights[name],
                pixels=self.tile_imgs[name]
            )
            for name in self.proto_tile_name_enum
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
        connector = self.sym_proto_tile_data[this_tile].constraints.get(direction)
        return {
            tile for tile in self.tile_name_enum
            if self.sym_proto_tile_data[tile].constraints.get(direction.reverse()) == connector
        }

    def symmetry_generators_from_symmetry_dict(self):
        return {
            name: TileSymmetryGenerator.from_symmetries(self.tile_symmetries[name])
            for name in self.proto_tile_name_enum
        }

    def symmetry_generators_from_constraints(self):
        return {
            name: TileSymmetryGenerator.from_constraint_symmetries(self.proto_tile_data[name].constraints)
            for name in self.proto_tile_name_enum
        }

    @abstractmethod
    def get_symmetry_generators(self):
        pass

    def symmetry_build(self):
        self.sym_gens = self.get_symmetry_generators()
        new_tile_names = set()
        for name in self.sym_gens.keys():
            new_tile_names = new_tile_names.union(self.sym_gens[name].generate_tile_names(name))
        self.tile_name_enum = Enum(self.SYM_PROTO_TILE_NAMES_ENUM_NAME, {name: name for name in new_tile_names})
        output_tiles = {}
        for name, tile_data in self.proto_tile_data.items():
            output_tiles.update(self.sym_gens[name].generate(self.tile_name_enum, tile_data))
        return output_tiles

    def get_tile_name(self, proto_tile_name: ProtoTileNames, g: GroupAction) -> TileNames:
        return self.tile_name_enum(
            TileSymmetryGenerator.transform_tile_name(g, proto_tile_name)
        )

    def get_tile_names(self, proto_tile_name: ProtoTileNames) -> Set[TileNames]:
        return {
            self.get_tile_name(proto_tile_name, g)
            for g in TileSymmetryGenerator(self.tile_symmetries[proto_tile_name]).transformations
        }
