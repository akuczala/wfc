import itertools

from cell import CollapsedCell, UncollapsedCell
from grid import Grid
from grid_array import GridArray
from grid_boundary import PeriodicGridBoundary, ConstantGridBoundary
from propagator import Propagator
from sub_grid import SubGrid
from tile_data.directed_pipe_data import DirectedPipeTileSet
from tile_data.pipe_data import PipeTileSet
from matplotlib import pyplot as plt

from tileset import TileSet


def make_grid(tileset: TileSet):

    width, height = 40, 40

    empty_tile = tileset.tile_name_enum('EMPTY_I')
    z4_names = ['I','S','SS','SSS']
    emitter_tiles = {tileset.tile_name_enum(f'EMITTER_{g}') for g in z4_names}
    consumer_tiles = {tileset.tile_name_enum(f'CONSUMER_{g}') for g in z4_names}

    grid = GridArray(width, height,
                boundary=ConstantGridBoundary(CollapsedCell(tileset.tile_data, empty_tile)),
                #boundary=PeriodicGridBoundary(),
                tile_data=tileset.tile_data,
                init_cell_factory=lambda: CollapsedCell(tileset.tile_data, empty_tile)
                #init_cell_factory=lambda: UncollapsedCell.with_any_tile(tileset)
                )

    init_cell_factory = lambda: UncollapsedCell.excluding_weight_zero(tileset)
    sub_grid = SubGrid(grid, (0, 0), (40, 40), tileset.tile_data,
                       init_cell_factory=init_cell_factory)
    place_emitter_consumer(tileset, grid)
    sub_grid.scanline_collapse()
    #collapse_animation_2(sub_grid, grid)

    # sub_grid = SubGrid(grid, (3, 3), (8, 8), tileset.tile_data,
    #                    init_cell_factory=init_cell_factory)
    # place_emitter_consumer(tileset, grid)
    # collapse_animation_2(sub_grid, grid)


    #grid.scanline_collapse()



    plt.imshow(grid.synthesize_img(), cmap='gray')
    plt.show()


def place_emitter_consumer(tileset, grid):
    emitter_tile = tileset.tile_name_enum('EMITTER_S')
    consumer_tile = tileset.tile_name_enum('CONSUMER_I')
    for (i, j), tile in zip(
            [(5, 5), (30, 30), (5, 30), (30, 5)],
            [consumer_tile, emitter_tile, consumer_tile, emitter_tile]
    ):
        grid.cells[i, j] = CollapsedCell(tileset.tile_data, tile)
        grid.collapse(i, j)


def collapse_animation(grid):
    for pos in grid.pos_iterator:
        #min_pos, min_val = grid.min_entropy_pos()
        #print(f"{min_val} at {min_pos}")
        grid.propagated_collapse(*pos)
        #grid.print_entropy()
        #print('-----')
        plt.imshow(grid.synthesize_img(), cmap='gray')
        plt.show()

def collapse_animation_2(update_grid, display_grid):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig = plt.figure()
    img = plt.imshow(display_grid.synthesize_img(), cmap='gray', animated=True)
    pos_iter = update_grid.pos_iterator

    def update(*args):
        pos = next(pos_iter)
        update_grid.propagated_collapse(*pos)
        img.set_array(display_grid.synthesize_img())
        return [img]

    try:
        ani = FuncAnimation(fig, update, frames=update_grid.width * update_grid.height, interval=10, blit=True, repeat=False)
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
