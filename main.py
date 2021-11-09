import itertools

from cell import CollapsedCell, UncollapsedCell
from grid import Grid
from grid_array import GridArray
from grid_boundary import PeriodicGridBoundary, ConstantGridBoundary
from propagator import Propagator
from tile_data.directed_pipe_data import DirectedPipeTileSet
from tile_data.pipe_data import PipeTileSet
from matplotlib import pyplot as plt

from tileset import TileSet


def make_grid(tileset: TileSet):

    width, height = 20, 20

    empty_tile = tileset.tile_name_enum('EMPTY_I')
    emitter_tile = tileset.tile_name_enum('EMITTER_S')
    consumer_tile = tileset.tile_name_enum('CONSUMER_I')

    grid = GridArray(width, height,
                #boundary=ConstantGridBoundary(CollapsedCell(tileset.tile_data, empty_tile)),
                boundary=PeriodicGridBoundary(),
                tile_data=tileset.tile_data,
                #init_cell_factory=lambda: CollapsedCell(tileset.tile_data, empty_tile)
                init_cell_factory=lambda: UncollapsedCell.with_any_tile(tileset)
                )

    # for (i, j) in itertools.product(range(10), range(10)):
    #     grid.cells[i, j] = UncollapsedCell(tileset.tile_data, {t for t in tileset.tile_name_enum})
    #     Propagator(grid).propagate_from(i, j)
    #     #plt.imshow(grid.synthesize_img(), cmap='gray')
    #     #plt.show()
    for (i, j), tile in zip([(5, 5), (15, 15)], [consumer_tile, emitter_tile]):
        grid.cells[i, j] = CollapsedCell(tileset.tile_data, tile)
        grid.collapse(i, j)

    grid.scanline_collapse()

    collapse_animation_2(grid)

    #plt.imshow(grid.synthesize_img(), cmap='gray')
    plt.show()

def collapse_animation(grid):
    for pos in grid.pos_iterator:
        #min_pos, min_val = grid.min_entropy_pos()
        #print(f"{min_val} at {min_pos}")
        grid.propagated_collapse(*pos)
        #grid.print_entropy()
        #print('-----')
        plt.imshow(grid.synthesize_img(), cmap='gray')
        plt.show()

def collapse_animation_2(grid):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig = plt.figure()
    img = plt.imshow(grid.synthesize_img(), cmap='gray', animated=True)
    pos_iter = grid.pos_iterator

    def update(*args):
        pos = next(pos_iter)
        grid.propagated_collapse(*pos)
        img.set_array(grid.synthesize_img())
        return [img]

    try:
        ani = FuncAnimation(fig, update, frames=grid.width * grid.height, interval=10, blit=True, repeat=False)
        plt.show()
    except StopIteration:
        pass

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
