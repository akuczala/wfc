from __future__ import annotations

import itertools
from abc import abstractmethod
from dataclasses import dataclass
from functools import reduce

from utils import signed_permutation_inverse_2x2
from typing import Set, Tuple

import numpy as np

BASE_MATRIX_MAP = {
    "I": (1, 0, 0, 1),
    "Tx": (-1, 0, 0, 1),
    "S": (0, -1, 1, 0),
    "Ty": (1, 0, 0, -1),
    "Txy": (0, 1, 1, 0)
}
MATRIX_NAMES = {
    t: name for name, t in BASE_MATRIX_MAP.items()
}


class GroupTargetMixin:
    @abstractmethod
    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        pass


class TrivialGroupTarget(GroupTargetMixin):

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self


@dataclass(frozen=True)
class GroupAction:
    matrix_elements: Tuple[int, int, int, int]

    @classmethod
    def from_matrix(cls, matrix: np.ndarray):
        assert matrix.dtype == np.int
        assert matrix.shape == (2, 2)
        return GroupAction(
            matrix_elements=tuple(x for x in matrix.ravel())
        )

    @property
    def matrix(self) -> np.ndarray:
        return np.array(self.matrix_elements).reshape(2, 2)

    @property
    def name(self):
        return MATRIX_NAMES[self.matrix_elements]

    def __mul__(self, other):
        return GroupAction.from_matrix(np.dot(self.matrix, other.matrix))

    def inverse(self):
        return GroupAction.from_matrix(signed_permutation_inverse_2x2(self.matrix))

    # def calc_order(self, max_order: int=10) -> int:

    def power_iterator(self):
        def power_generator(a):
            yield Group.id()
            g = a
            while g != Group.id():
                yield g
                g = g * a

        return iter(power_generator(self))

    def __eq__(self, other):
        return self.matrix_elements == other.matrix_elements

    def __hash__(self):
        return self.matrix_elements.__hash__()


class Group:
    @staticmethod
    def id():
        return GroupAction(BASE_MATRIX_MAP["I"])

    @staticmethod
    def rot90():
        return GroupAction(BASE_MATRIX_MAP["S"])

    @staticmethod
    def flip_y():
        return GroupAction(BASE_MATRIX_MAP["Ty"])

    @staticmethod
    def flip_x():
        return GroupAction(BASE_MATRIX_MAP["Tx"])

    @staticmethod
    def swap_xy():
        return GroupAction(BASE_MATRIX_MAP["Txy"])

    def get_elements(self) -> Set[GroupAction]:
        pass

    def __len__(self):
        return len(self.get_elements())


@dataclass
class GeneratedGroup(Group):
    generators: Set[GroupAction]

    def get_elements(self) -> Set[GroupAction]:
        return {
            reduce(lambda g1, g2: g1 * g2, g_tuple)
            for g_tuple in itertools.product(*(gen.power_iterator() for gen in self.generators))
        }


@dataclass
class Trivial(Group):
    def get_elements(self) -> Set[GroupAction]:
        return {Group.id()}


Z4_SQUARE = GeneratedGroup({Group.rot90()})
D4_SQUARE = GeneratedGroup({Group.rot90(), Group.flip_x()})

# todo generalize
_s = Group.rot90()
_t = Group.flip_x()
for (g1, g2) in ((_s, _s), (_s * _s, _s), (_s, _t), (_s * _s, _t), (_s * _s * _s, _t)):
    MATRIX_NAMES[(g1 * g2).matrix_elements] = f"{g1.name}{g2.name}"
