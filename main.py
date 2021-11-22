from grid.cell import CollapsedCell, UncollapsedCell
from grid.grid_array import GridArray
from grid.grid_boundary import ConstantGridBoundary, PeriodicGridBoundary
from grid.sub_grid import SubGrid
from symmetry.planar_groups import PlanarGroupAction
from symmetry.cubic_groups import CUBIC_GROUP
from tile_data.connectors import PipeProtoConnectors
from tile_data.directed_pipe_data import DirectedPipeTileSet
from matplotlib import pyplot as plt

from tile_data.pipe_data import PipeTileSet
from tile_data.zelda_data import ZeldaTileSet
from tile_data.zelda_two_level import Zelda2TileSet
from tileset import TileSet


def make_generic_grid(tileset: TileSet):
    width, height = 20, 20
    grid = GridArray((width, height),
                     boundary=ConstantGridBoundary(UncollapsedCell.with_any_tile(tileset)),
                     #boundary=PeriodicGridBoundary(),
                     tile_data=tileset.tile_data,
                     init_cell_factory=lambda: UncollapsedCell.with_any_tile(tileset)
                     )
    collapse_animation_2(grid, grid)

    # grid.scanline_collapse()
    # plt.imshow(grid.synthesize_img(), cmap='gray')
    # plt.show()


def make_directed_pipe_grid():
    tileset = DirectedPipeTileSet()
    width, height = 20, 20

    # todo fix get tile name
    empty_tile = tileset.get_tile_name(
        DirectedPipeTileSet.proto_tile_name_enum.EMPTY,
        PlanarGroupAction.rot90() * PlanarGroupAction.rot90()
    )
    #emitter_tiles = tileset.get_tile_names(DirectedPipeTileSet.proto_tile_name_enum.EMITTER)
    #consumer_tiles = tileset.get_tile_names(DirectedPipeTileSet.proto_tile_name_enum.CONSUMER)

    grid = GridArray((width, height),
                     boundary=ConstantGridBoundary(CollapsedCell(tileset.tile_data, empty_tile)),
                     # boundary=PeriodicGridBoundary(), # todo: not working properly with sub grid
                     tile_data=tileset.tile_data,
                     init_cell_factory=lambda: CollapsedCell(tileset.tile_data, empty_tile)
                     # init_cell_factory=lambda: UncollapsedCell.with_any_tile(tileset)
                     )

    init_cell_factory = lambda: UncollapsedCell.excluding_weight_zero(tileset)
    sub_grid = SubGrid(grid, (0, 0), (20, 20), tileset.tile_data,
                       init_cell_factory=init_cell_factory)
    #place_emitter_consumer(tileset, grid)
    # sub_grid.scanline_collapse()
    collapse_animation_2(sub_grid, grid)

    # sub_grid = SubGrid(grid, (3, 3), (8, 8), tileset.tile_data,
    #                    init_cell_factory=init_cell_factory)
    # place_emitter_consumer(tileset, grid)
    # collapse_animation_2(sub_grid, grid)

    # grid.scanline_collapse()

    plt.imshow(grid.synthesize_img(), cmap='gray')
    plt.show()


def place_emitter_consumer(tileset, grid):
    emitter_tile = next(iter(tileset.get_tile_names(DirectedPipeTileSet.proto_tile_name_enum.EMITTER)))
    consumer_tile = next(iter(tileset.get_tile_names(DirectedPipeTileSet.proto_tile_name_enum.CONSUMER)))
    for (i, j), tile in zip(
            [(5, 5), (15, 15), (6, 14), (13, 4)],
            [emitter_tile, consumer_tile, emitter_tile, consumer_tile]
    ):
        grid.cells[i, j] = CollapsedCell(tileset.tile_data, tile)
        grid.collapse(i, j)


def collapse_animation(grid):
    for pos in grid.pos_iterator:
        # min_pos, min_val = grid.min_entropy_pos()
        # print(f"{min_val} at {min_pos}")
        grid.propagated_collapse(*pos)
        # grid.print_entropy()
        # print('-----')
        plt.imshow(grid.synthesize_img(), cmap='gray')
        plt.show()


def collapse_animation_2(update_grid, display_grid):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig = plt.figure()
    img = plt.imshow(display_grid.synthesize_img(), cmap='gray', animated=True)
    pos_iter = update_grid.pos_iterator

    # pos_iter = update_grid.min_entropy_pos_iterator

    def update(*args):
        pos = next(pos_iter)
        update_grid.propagated_collapse(pos)
        img.set_array(display_grid.synthesize_img())
        return [img]

    try:
        ani = FuncAnimation(fig, update, frames=update_grid.shape[0] * update_grid.shape[1], interval=10, blit=True,
                            repeat=False)
        plt.show()
    except StopIteration:
        pass


def pixel_test(tileset):
    tile_I = tileset.tile_name_enum('4_I')
    tile_Tx = tileset.tile_name_enum('4_ITx')
    tile_S = tileset.tile_name_enum('4_S')
    plt.imshow(tileset.tile_data[tile_I].pixels);
    plt.show()
    plt.imshow(tileset.tile_data[tile_S].pixels);
    plt.show()


make_directed_pipe_grid()
#make_generic_grid(PipeTileSet())
#constraint_symmetry()
pass
