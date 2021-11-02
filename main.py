from cell import CollapsedCell
from grid import Grid
from tile_data.directed_pipe_data import DirectedPipeTileSet
from tile_data.pipe_data import PipeTileSet
from matplotlib import pyplot as plt

from tileset import TileSet


def make_grid(tileset: TileSet):

    width, height = 10, 10
    grid = Grid(width, height, tileset.tile_data)

    emitter_tile = tileset.tile_name_enum('5_I')
    consumer_tile = tileset.tile_name_enum('6_I')
    for (i, j), tile in zip([(2, 2), (7, 7)], [emitter_tile, consumer_tile]):
        grid.cells[i, j] = CollapsedCell(tileset.tile_data, tile)
        grid.collapse(i, j)

    #grid.collapse_all()

    #grid.print()

    for _ in range(100):
        min_pos, min_val = grid.min_entropy_pos()
        print(f"{min_val} at {min_pos}")
        grid.propagated_collapse(*min_pos)
        grid.print_entropy()
        print('-----')
        plt.imshow(grid.synthesize_img(), cmap='gray')
        plt.show()

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
