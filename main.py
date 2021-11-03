import itertools

from cell import CollapsedCell
from grid import Grid
from tile_data.directed_pipe_data import DirectedPipeTileSet
from tile_data.pipe_data import PipeTileSet
from matplotlib import pyplot as plt

from tileset import TileSet


def make_grid(tileset: TileSet):

    width, height = 20, 20
    grid = Grid(width, height, tileset.tile_data, False)
    boundary_tile = tileset.tile_name_enum('1_I')
    if not grid.periodic:
        for (i, j) in itertools.product(range(grid.width), (0, grid.height - 1)):
            grid.cells[i, j] = CollapsedCell(tileset.tile_data, boundary_tile)
            grid.collapse(i, j)
            #show_grid(grid)
        for (i, j) in itertools.product((0, grid.width - 1), range(grid.height)):
            grid.cells[i, j] = CollapsedCell(tileset.tile_data, boundary_tile)
            grid.collapse(i, j)
            #show_grid(grid)

    emitter_tile = tileset.tile_name_enum('5_I')
    consumer_tile = tileset.tile_name_enum('6_I')
    for (i, j), tile in zip([(2, 2), (7, 7)], [emitter_tile, consumer_tile]):
        grid.cells[i, j] = CollapsedCell(tileset.tile_data, tile)
        grid.collapse(i, j)

    grid.collapse_all()
    show_grid(grid)

    #grid.print()

    # for _ in range(100):
    #     min_pos, min_val = grid.min_entropy_pos()
    #     print(f"{min_val} at {min_pos}")
    #     grid.collapse(*min_pos)
    #     #grid.print_entropy()
    #     print('-----')
    #     show_grid(grid)



def show_grid(grid):
    plt.imshow(grid.synthesize_img(), cmap='gray')
    plt.show()

def pixel_test(tileset):
    tile_I = tileset.tile_name_enum('4_I')
    tile_Tx = tileset.tile_name_enum('4_ITx')
    tile_S = tileset.tile_name_enum('4_S')
    plt.imshow(tileset.tile_data[tile_I].pixels); plt.show()
    plt.imshow(tileset.tile_data[tile_S].pixels); plt.show()

tileset = DirectedPipeTileSet()
make_grid(tileset)
#pixel_test(tileset)
pass
