from typing import Dict

import numpy as np

from connectors import Connectors
from directions import Directions
from tiles import ProtoTileNames, ProtoTileData


class PipeProtoTileNames(ProtoTileNames):
    EMPTY = ' '
    HORIZONTAL_PIPE = '-'
    VERTICAL_PIPE = '|'
    CROSS_PIPE = '+'
    ANGLE_PIPE_1 = 'a'
    ANGLE_PIPE_2 = 'b'
    ANGLE_PIPE_3 = 'c'
    ANGLE_PIPE_4 = 'd'
    TERMINAL = 't'


def build_proto_data() -> Dict[ProtoTileNames, ProtoTileData]:
    tile_constraints = {
        PipeProtoTileNames.EMPTY: {
            Directions.UP: Connectors.NONE,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.NONE,
        },
        PipeProtoTileNames.HORIZONTAL_PIPE: {
            Directions.UP: Connectors.NONE,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.HORIZONTAL,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.VERTICAL_PIPE: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.VERTICAL,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.NONE,
        },
        PipeProtoTileNames.CROSS_PIPE: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.VERTICAL,
            Directions.LEFT: Connectors.HORIZONTAL,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.ANGLE_PIPE_1: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.ANGLE_PIPE_2: {
            Directions.UP: Connectors.NONE,
            Directions.DOWN: Connectors.VERTICAL,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.HORIZONTAL,
        },
        PipeProtoTileNames.ANGLE_PIPE_3: {
            Directions.UP: Connectors.NONE,
            Directions.DOWN: Connectors.VERTICAL,
            Directions.LEFT: Connectors.HORIZONTAL,
            Directions.RIGHT: Connectors.NONE,
        },
        PipeProtoTileNames.ANGLE_PIPE_4: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.HORIZONTAL,
            Directions.RIGHT: Connectors.NONE,
        },
        PipeProtoTileNames.TERMINAL: {
            Directions.UP: Connectors.VERTICAL,
            Directions.DOWN: Connectors.NONE,
            Directions.LEFT: Connectors.NONE,
            Directions.RIGHT: Connectors.NONE,
        }
    }
    tile_weights = {
        PipeProtoTileNames.EMPTY: 80,
        PipeProtoTileNames.HORIZONTAL_PIPE: 3,
        PipeProtoTileNames.VERTICAL_PIPE: 3,
        PipeProtoTileNames.CROSS_PIPE: 0.5,
        PipeProtoTileNames.ANGLE_PIPE_1: 1,
        PipeProtoTileNames.ANGLE_PIPE_2: 1,
        PipeProtoTileNames.ANGLE_PIPE_3: 1,
        PipeProtoTileNames.ANGLE_PIPE_4: 1,
        PipeProtoTileNames.TERMINAL: 0.0
    }
    tile_imgs = {
        PipeProtoTileNames.EMPTY: np.array([
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]),
        PipeProtoTileNames.HORIZONTAL_PIPE: np.array([
            [0,0,0],
            [1,1,1],
            [0,0,0]
        ]),
        PipeProtoTileNames.VERTICAL_PIPE: np.array([
            [0,1,0],
            [0,1,0],
            [0,1,0]
        ]),
        PipeProtoTileNames.CROSS_PIPE: np.array([
            [0,1,0],
            [1,1,1],
            [0,1,0]
        ]),
        PipeProtoTileNames.ANGLE_PIPE_1: np.array([
            [0,1,0],
            [0,1,1],
            [0,0,0]
        ]),
        PipeProtoTileNames.ANGLE_PIPE_2: np.array([
            [0,0,0],
            [0,1,1],
            [0,1,0]
        ]),
        PipeProtoTileNames.ANGLE_PIPE_3: np.array([
            [0,0,0],
            [1,1,0],
            [0,1,0]
        ]),
        PipeProtoTileNames.ANGLE_PIPE_4: np.array([
            [0,1,0],
            [1,1,0],
            [0,0,0]
        ]),
        PipeProtoTileNames.TERMINAL: np.array([
            [0,1,0],
            [0,1,0],
            [0,0,0]
        ]),
    }
    return {
        name: ProtoTileData(
            name=name,
            constraints=tile_constraints[name],
            weight=tile_weights[name],
            pixels=tile_imgs[name]
        )
        for name in PipeProtoTileNames
    }