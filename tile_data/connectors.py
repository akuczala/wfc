from enum import Enum, auto

from abc_enum import ABCEnumMeta
from connectors import ProtoConnectors


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


class Zelda2ProtoConnectors(ProtoConnectors, Enum, metaclass=ABCEnumMeta):
    BRIDGE = auto()
    WALL = auto()
    LOWER = auto()
    UPPER = auto()