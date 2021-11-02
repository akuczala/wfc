from directions import Directions


class Propagator:
    def __init__(self, grid):
        self.stack = []
        self.grid = grid
    def constrain(self, i, j):
        #print(i,j)
        for direction in Directions:
            compatible_tiles = self.grid.cells[i,j].get_compatible_tiles(direction)
            ni, nj = self.grid.neighbor(i, j, direction)
            prev_len = len(self.grid.cells[ni,nj].tiles)
            self.grid.cells[ni,nj] = self.grid.cells[ni,nj].constrain(compatible_tiles)
            new_len = len(self.grid.cells[ni,nj].tiles)
            if new_len != prev_len:
                #print(f'add {(ni, nj)} to stack')
                self.stack.append((ni, nj))
    def propagate_from(self, i, j):
        self.stack = [(i,j)]
        while len(self.stack) > 0:
            self.constrain(*self.stack.pop())
            #print(self.stack)