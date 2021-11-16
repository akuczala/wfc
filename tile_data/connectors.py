import itertools
from enum import Enum, auto
from typing import Optional

from abc_enum import ABCEnumMeta
from connectors import Connectors, ProtoConnectors
from directions import Directions
from symmetry.groups import GroupAction
from utils import optional_map


class PipeProtoConnectors(ProtoConnectors, Enum, metaclass=ABCEnumMeta):
    HORIZONTAL = 'HORIZONTAL'
    NONE = 'NONE'


class DirectedPipeProtoConnectors(ProtoConnectors, Enum, metaclass=ABCEnumMeta):
    UP = 'UP'
    NONE = 'NONE'


class ZeldaProtoConnectors(ProtoConnectors, Enum, metaclass=ABCEnumMeta):
    BRIDGE = auto()
    WALL = auto()
    NONE = auto()


class Zelda2Connectors(Connectors, Enum, metaclass=ABCEnumMeta):
    WALL_BOUNDARY_HORIZONTAL = auto()
    WALL_BOUNDARY_VERTICAL = auto()
    BRIDGE_HORIZONTAL = auto()
    BRIDGE_VERTICAL = auto()
    WALL_HORIZONTAL = auto()
    WALL_VERTICAL = auto()
    LOWER = auto()
    UPPER = auto()

    def transform(self, g_action: GroupAction) -> Connectors:
        if g_action.matrix[0, 1] != 0:  # off-diagonal element implies x<->y
            hv_pairs = (
                (self.WALL_HORIZONTAL, self.WALL_VERTICAL),
                (self.WALL_BOUNDARY_HORIZONTAL, self.WALL_BOUNDARY_VERTICAL),
                (self.BRIDGE_HORIZONTAL, self.BRIDGE_VERTICAL),
                (self.LOWER, self.LOWER),
                (self.UPPER, self.UPPER)
            )
            return {
                key: val
                for key, val in itertools.chain(((h, v) for h, v in hv_pairs), ((v, h) for h, v in hv_pairs))
            }[self]
        else:
            return self
