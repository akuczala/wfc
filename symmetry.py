from dataclasses import dataclass
from enum import Enum
from utils import singledispatchmethod, transform_pixels
from typing import Dict, Set

import numpy as np

from connectors import Connectors
from directions import Directions
from tiles import ProtoTileData, ProtoTileNames


class GroupAction:
    def __init__(self, name, matrix):
        self.matrix = matrix
        self.name = name

    @singledispatchmethod
    def transform(self, x):
        raise TypeError(f"GroupAction cannot transform {x} which is of type {type(x)}")

    @transform.register
    def _(self, x: Directions):
        return Directions.arr_to_dir(np.dot(self.matrix, np.array(x.value)))

    @transform.register
    def _(self, x: Connectors):
        return x.transform(self)

    @transform.register
    def _(self, x: np.ndarray):
        if x.shape[0] != x.shape[1]:
            raise TypeError(f"Cannot transform non-square pixel array; found shape {x.shape}")
        return transform_pixels(self.matrix, x)

    def __mul__(self, other):
        return GroupAction(self.name + other.name, np.dot(self.matrix, other.matrix))


class Group:
    @staticmethod
    def id():
        return GroupAction("I", np.eye(2, dtype=np.int))

    @staticmethod
    def rot90():
        return GroupAction("S", np.array([[0, -1], [1, 0]]))

    @staticmethod
    def flip_y():
        return GroupAction("Ty", np.array([[1, 0], [0, -1]]))

    @staticmethod
    def flip_x():
        return GroupAction("Tx", np.array([[-1, 0], [0, 1]]))

    @staticmethod
    def swap_xy():
        return GroupAction("Txy", np.array([[0, 1], [1, 0]]))

    def get_elements(self) -> Set[GroupAction]:
        pass

    def __len__(self):
        return len(self.get_elements())


@dataclass
class Trivial(Group):
    def get_elements(self) -> Set[GroupAction]:
        return {Group.id()}

@dataclass
class K4(Group):
    t1: GroupAction
    t2: GroupAction

    def get_elements(self):
        t1, t2 = self.t1, self.t2
        return {Group.id(), t1, t2, t1 * t2}


@dataclass
class Z2(Group):
    t: GroupAction

    def get_elements(self):
        return {Group.id(), self.t}


@dataclass
class Z4(Group):
    s: GroupAction

    def get_elements(self):
        s = self.s
        return {Group.id(), s, s * s, s * s * s}


@dataclass
class D4(Group):
    s: GroupAction
    t: GroupAction

    def get_elements(self):
        s = self.s
        t = self.t
        return Z4(s).get_elements().union({z * t for z in Z4(s).get_elements()})


Z4_SQUARE = Z4(Group.rot90())
D4_SQUARE = D4(Group.rot90(), Group.flip_x())

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

