from cell import CollapsedCell
from grid import Grid
from tile_data.pipe_data import PipeTileSet
from matplotlib import pyplot as plt

from tileset import TileSet


def make_grid(tileset: TileSet):

    width, height = 20, 20
    grid = Grid(width, height, tileset.tile_data)

    terminal_tile = tileset.tile_name_enum('t_I')
    for (i, j) in [(5, 5), (15, 15)]:
        grid.cells[i, j] = CollapsedCell(tileset.tile_data, terminal_tile)
        grid.collapse(i, j)

    grid.collapse_all()

    #grid.print()
    plt.imshow(grid.synthesize_img())
    plt.show()
    # for row in grid.synthesize_img():
    #     print("".join(['O' if v == 1 else ' ' for v in row]))


# proto_tile_data = build_proto_data()
# print(transform_pixels(Group.flip_x().matrix, proto_tile_data[PipeProtoTileNames.ANGLE_PIPE_1].pixels))


make_grid(PipeTileSet())
pass
