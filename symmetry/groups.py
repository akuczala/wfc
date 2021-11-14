from dataclasses import dataclass
from utils import singledispatchmethod, transform_pixels, signed_permutation_inverse_2x2
from typing import Dict, Set

import numpy as np

from connectors import Connectors
from directions import Directions


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

    def inverse(self):
        return GroupAction(f"({self.name})^(-1)", signed_permutation_inverse_2x2(self.matrix))


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


