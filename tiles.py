from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set

import numpy as np

from connectors import Connectors
from directions import Directions, Directions2D, Directions3D
from symmetry.groups import GroupTargetMixin, GroupAction
from utils import transform_pixels


class ProtoTileNames(Enum):

    def get_all_tiles(self):
        return {t for t in self}


@dataclass
class TilePixels(GroupTargetMixin):
    array: np.ndarray

    def transform(self, g_action: GroupAction) -> TilePixels:
        return transform_pixels(g_action.matrix, self.array)


@dataclass(frozen=True)
class TileConstraints(GroupTargetMixin):
    constraint_dict: Dict[Directions, Connectors]

    def transform(self, g_action: GroupAction) -> TileConstraints:
        return TileConstraints(
            constraint_dict={
                direction.transform(g_action): connector.transform(g_action)
                for direction, connector in self.constraint_dict.items()
            }
        )

    def get(self, direction: Directions) -> Connectors:
        return self.constraint_dict[direction]

    def get_map(self) -> Dict[Directions, Connectors]:
        return self.constraint_dict

    @staticmethod
    def make_constraints_2d(up: Connectors, down: Connectors, left: Connectors, right: Connectors) -> TileConstraints:
        return TileConstraints(constraint_dict={
            Directions2D.UP: up,
            Directions2D.DOWN: down,
            Directions2D.LEFT: left,
            Directions2D.RIGHT: right
        })

    @staticmethod
    def make_constraints_3d(
            up: Connectors, down: Connectors, left: Connectors, right: Connectors,
            in_: Connectors, out: Connectors) -> TileConstraints:
        return TileConstraints(constraint_dict={
            Directions3D.UP: up,
            Directions3D.DOWN: down,
            Directions3D.LEFT: left,
            Directions3D.RIGHT: right,
            Directions3D.IN: in_,
            Directions3D.OUT: out
        })


@dataclass
class ProtoTileData:
    constraints: TileConstraints
    weight: float
    name: ProtoTileNames
    pixels: TilePixels


@dataclass
class SymmetryGeneratedProtoTileData(ProtoTileData, GroupTargetMixin):
    g_target: GroupTargetMixin

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return SymmetryGeneratedProtoTileData(
            constraints=self.constraints.transform(g_action),
            weight=self.weight,
            name=self.name,
            pixels=self.pixels.transform(g_action),
            g_target=self.g_target.transform(g_action)
        )


def random_tile(tile_data, tiles):
    tile_list = list(tiles)
    probs = np.array([tile_data[t].weight for t in tile_list])
    probs = probs / sum(probs)
    return np.random.choice(tile_list, p=probs)


class TileNames:
    pass


@dataclass
class TileData:
    name: TileNames
    weight: float
    compatible_tiles: Dict[Directions, Set[TileNames]]
    pixels: Set[TileNames]
