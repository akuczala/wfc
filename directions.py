from enum import Enum

import numpy as np

from symmetry.groups import GroupTargetMixin, GroupAction


class Directions(GroupTargetMixin, Enum):
    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]

    def reverse(self):
        return Directions([-x for x in self.value])

    @staticmethod
    def arr_to_dir(arr):
        return Directions([int(x) for x in arr])

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self.arr_to_dir(np.dot(g_action.matrix, np.array(self.value)))
