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


class PipeConnectors(Connectors, Enum, metaclass=ABCEnumMeta):
    HORIZONTAL = 'h'
    VERTICAL = 'v'
    NONE = 'n'

    def transform(self, g_action: GroupAction) -> Connectors:
        if g_action.matrix[0, 1] != 0: #off-diagonal element implies x<->y
            return {
                PipeConnectors.HORIZONTAL: PipeConnectors.VERTICAL,
                PipeConnectors.VERTICAL: PipeConnectors.HORIZONTAL,
                PipeConnectors.NONE: PipeConnectors.NONE
            }[self]
        else:
            return self


class DirectedPipeConnectors(Connectors, Enum, metaclass=ABCEnumMeta):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    NONE = auto()

    def to_direction(self) -> Optional[Directions]:
        return {
            self.UP: Directions.UP,
            self.DOWN: Directions.DOWN,
            self.LEFT: Directions.LEFT,
            self.RIGHT: Directions.RIGHT,
            self.NONE: None
        }[self]

    @classmethod
    def from_direction(cls, direction: Optional[Directions]) -> "DirectedPipeConnectors":
        return {
            Directions.UP: cls.UP,
            Directions.DOWN: cls.DOWN,
            Directions.LEFT: cls.LEFT,
            Directions.RIGHT: cls.RIGHT,
            None: cls.NONE
        }[direction]

    def transform(self, g_action: GroupAction) -> Connectors:
        return self.from_direction(
            optional_map(g_action.transform, self.to_direction())
        )

class ZeldaConnectors(Connectors, Enum, metaclass=ABCEnumMeta):
    WALL_BOUNDARY_HORIZONTAL = auto()
    WALL_BOUNDARY_VERTICAL = auto()
    BRIDGE_HORIZONTAL = auto()
    BRIDGE_VERTICAL = auto()
    WALL_HORIZONTAL = auto()
    WALL_VERTICAL = auto()
    NONE = auto()

    def transform(self, g_action: GroupAction) -> Connectors:
        if g_action.matrix[0, 1] != 0:  # off-diagonal element implies x<->y
            hv_pairs = (
                    (self.WALL_HORIZONTAL, self.WALL_VERTICAL),
                    (self.WALL_BOUNDARY_HORIZONTAL, self.WALL_BOUNDARY_VERTICAL),
                    (self.BRIDGE_HORIZONTAL, self.BRIDGE_VERTICAL),
                    (self.NONE, self.NONE)
                )
            return {
                key: val
                for key, val in itertools.chain(((h,v) for h,v in hv_pairs),((v,h) for h,v in hv_pairs))
            }[self]
        else:
            return self


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
                for key, val in itertools.chain(((h,v) for h,v in hv_pairs),((v,h) for h,v in hv_pairs))
            }[self]
        else:
            return self