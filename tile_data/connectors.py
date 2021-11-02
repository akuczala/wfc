from enum import Enum, auto
from typing import Optional

from connectors import Connectors
from directions import Directions
from symmetry import GroupAction
from utils import optional_map


class PipeConnectors(Connectors, Enum):
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


class DirectedPipeConnectors(Connectors, Enum):
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