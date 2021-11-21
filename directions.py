from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

import numpy as np

from symmetry.groups import GroupTargetMixin, GroupAction


# todo rename to Direction (singular)
class Directions(GroupTargetMixin, ABC):

    def __init__(self, value: Tuple[int, ...]):
        self.value = value

    def reverse(self):
        return Directions(tuple(-x for x in self.value))

    @staticmethod
    def arr_to_dir(arr):
        return Directions(tuple(int(x) for x in arr))

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self.arr_to_dir(np.dot(g_action.matrix, np.array(self.value)))

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Directions2D:
    UP = Directions((-1, 0))
    DOWN = Directions((1, 0))
    LEFT = Directions((0, -1))
    RIGHT = Directions((0, 1))

    def __iter__(self):
        for d in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
            yield d


class Directions3D:
    UP = Directions((-1, 0, 0))
    DOWN = Directions((1, 0, 0))
    LEFT = Directions((0, -1, 0))
    RIGHT = Directions((0, 1, 0))
    IN = Directions((0, 0, 1))
    OUT = Directions((0, 0, -1))

    def __iter__(self):
        for d in [self.UP, self.DOWN, self.LEFT, self.RIGHT, self.IN, self.OUT]:
            yield d


DIRECTIONS_DIM_MAP = {
    2: Directions2D(),
    3: Directions3D()
}
