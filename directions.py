from enum import Enum


class Directions(Enum):
    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]

    def reverse(self):
        return Directions([-x for x in self.value])

    @staticmethod
    def arr_to_dir(arr):
        return Directions([int(x) for x in arr])
