import random
from .description_generator import gen_room_desc

class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.rooms = {}

    def calculate_room_direction(self, room, previous_room):
        """
        Calculates the relationship between a new room and the previous room.
        """
        if previous_room == None:
            return None
        prev_x = previous_room.x
        prev_y = previous_room.y

        current_x = room.x
        current_y = room.y

        if current_x == prev_x:
            if current_y > prev_y:
                return 'n'
            else:
                return 's'
        else:
            if current_x > prev_x:
                return 'e'
            else:
                return 'w'
       

    def depth_first_room_generator(self, size_x, size_y):
        '''
        Depth first room generator.
        '''
        MAZE_HEIGHT = size_y
        MAZE_WIDTH = size_x

        def _create_grid_with_cells(width, height):
            """ Create a grid with empty cells on odd row/column combinations. """
            grid = []
            for row in range(height):
                grid.append([])
                for column in range(width):
                    if column % 2 == 1 and row % 2 == 1:
                        grid[row].append((column, row))
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
                        maze[max(y, yy) * 2][x * 2 + 1] = (max(y, yy) * 2, x * 2 + 1)
                    if yy == y:
                        maze[y * 2 + 1][max(x, xx) * 2] = (y * 2 + 1, max(x, xx) * 2)

                    walk(xx, yy)

            walk(random.randrange(w), random.randrange(h))

            for line in maze:
                print(line)

            return maze

        # create a grid of coords and 0s that can be populated with rooms
        self.grid = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)

        def populate_maze():
            """ Traverses the maze object and turns 1s into rooms then connects them"""
            room_count = 1
            room_descriptions = gen_room_desc()

            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 0:
                        self.grid[i][j] = None
                    else:
                        # generate room
                        x = self.grid[i][j][0] - 1
                        y = self.grid[i][j][1] - 1
                        
                        # print(x,y, len(self.grid))

                        # get a description
                        desc = room_descriptions.pop()

                        room = Room(room_count, desc['name'], desc['desc'], x, y)
            
                        # save the room in the grid and in a dict
                        self.grid[i][j] = room
                        self.rooms[room_count] = room
                        
                        room_count += 1

            # Now we have filled the grid with rooms, we connect them
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == None:
                        pass
                    else:
                        #scan nearby rooms and connect them
                        adj_rooms = [(i-1, j), (i + 1, j), (i, j-1), (i, j+1)]
                        for room in adj_rooms:
                            if (room[0] in range(len(self.grid))) and (room[1] in range(len(self.grid[i]))):

                                if self.grid[room[0]][room[1]] != None:
                                    direction = self.calculate_room_direction(self.grid[i][j], self.grid[room[0]][room[1]])
                                    self.grid[room[0]][room[1]].connect_rooms(self.grid[i][j], direction)
            
            print(f'room count {room_count}')
        
        populate_maze()

#### Usage Example ####

# w = World()
# width = 11
# height = 11
# w.depth_first_room_generator(width, height)
# for line in w.grid:
#     print(line)
