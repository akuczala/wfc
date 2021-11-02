from enum import Enum

import numpy as np

from cell import CollapsedCell
from grid import Grid
from symmetry import TileSymmetryGenerator, Z2, Group
from tile_data import build_proto_data
from tiles import generate_compatible_tiles, ProtoTileNames, PipeProtoTileNames
from utils import transform_pixels


def symmetry_build():
    proto_tile_data = build_proto_data()
    tile_data = proto_tile_data[PipeProtoTileNames.HORIZONTAL_PIPE]
    sym_gen = TileSymmetryGenerator(Z2(Group.swap_xy()))
    new_tile_names = sym_gen.generate_tile_names(tile_data)
    SymProtoTileNames = Enum('SymProtoTileNames', {name: name for name in new_tile_names})
    return sym_gen.generate(SymProtoTileNames, tile_data)

def make_grid():
    proto_tile_data = build_proto_data()
    tile_data = generate_compatible_tiles(proto_tile_data)

    width, height = 20, 20
    grid = Grid(width, height, tile_data)
    for (i, j) in [(5, 5), (15, 15)]:
        grid.cells[i, j] = CollapsedCell(tile_data, PipeProtoTileNames.TERMINAL)
        grid.collapse(i, j)

    grid.collapse_all()

    grid.print()

sym_tiles = symmetry_build()
# proto_tile_data = build_proto_data()
# print(transform_pixels(Group.flip_x().matrix, proto_tile_data[PipeProtoTileNames.ANGLE_PIPE_1].pixels))
make_grid()
pass