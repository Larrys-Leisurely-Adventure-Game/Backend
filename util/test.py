
import random

MAZE_HEIGHT = 11
MAZE_WIDTH = 11

def _create_grid_with_cells(width, height):
    """ Create a grid with empty cells on odd row/column combinations. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(1)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(0)
            else:
                grid[row].append(0)
    return grid


def make_maze_depth_first(maze_width, maze_height):
    maze = _create_grid_with_cells(maze_width, maze_height)

    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x: int, y: int):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = 1
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = 1

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))

    return maze

m = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)

for line in m:
    print(line)