from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

import numpy as np

from symmetry.groups import GroupTargetMixin, MatrixGroupAction, GroupAction
from tiles.names import ProtoTileNames
from utils import is_even


class TileGraphics(GroupTargetMixin, ABC):
    pass


class NoTileGraphics(TileGraphics):

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self


@dataclass
class MatrixActionGraphics(TileGraphics):
    action: MatrixGroupAction
    name: ProtoTileNames

    def transform(self, g_action: GroupAction) -> GroupTargetMixin:
        return self.__class__(name=self.name, action=g_action * self.action)


@dataclass
class TilePixels(TileGraphics):
    array: np.ndarray

    def transform(self, g_action: MatrixGroupAction) -> TilePixels:
        return self.__class__(self._transform_pixel_array(g_action.matrix))

    def _transform_pixel_array(self, transform: np.ndarray):
        pixels = self.array
        n = pixels.shape[0]
        transformed_index = np.array(
            [
                np.ravel_multi_index(
                    self.pos_to_pixel_coord(
                        *np.dot(transform.T,
                                np.array(self.pixel_coord_to_pos(*np.unravel_index(idx, pixels.shape), n))),
                        n
                    ), pixels.shape
                )
                for idx in range(n * n)]
        )
        return pixels.ravel()[transformed_index].reshape(pixels.shape)

    @staticmethod
    def pixel_coord_to_pos(i, j, n):
        shift = n - 1 if is_even(n) else (n - 1) // 2
        scale = 2 if is_even(n) else 1
        return i * scale - shift, j * scale - shift

    @staticmethod
    def pos_to_pixel_coord(x, y, n):
        shift = n - 1 if is_even(n) else (n - 1) // 2
        scale = 2 if is_even(n) else 1
        return (x + shift) // scale, (y + shift) // scale
