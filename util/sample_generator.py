# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

import random


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
        self.grid = []
        room_count = 0
        previous_room = None

        # populate grid with rooms
        for row in range(size_y):
            self.grid.append([])

            for column in range(size_x):

                if column % 2 == 1 and row % 2 == 1:
                                     

                    room = Room(room_count, "A Generic Room", "This is a generic room.", column, row)

                    

                    self.grid[row].append(room)

                    if previous_room is not None:
                        room_direction = self.calculate_room_direction(room, previous_room)
                        previous_room.connect_rooms(room, room_direction)

                    # Update iteration variables
                    previous_room = room
                    room_count += 1
                elif column == 0 or row == 0 or column == size_x -1 or row == size_y -1:
                    #wall = Wall(#TODO)
                    self.grid[row].append(None)
                else:
                    #wall = Wall(#TODO)
                    self.grid[row].append(None)

        # now do a depth first traversal
        w = (len(self.grid[0]) - 1) // 2
        h = (len(self.grid) - 1) // 2
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

        def walk(x: int, y: int, room_count):
            vis[y][x] = 1
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            random.shuffle(d)
            previous_room = None
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    room = Room(room_count, "A Generic Room", "This is a generic room.", column, row)

                    self.grid[max(y, yy) * 2][x * 2 + 1] = room

                    if previous_room is not None:
                        room_direction = self.calculate_room_direction(room, previous_room)
                        previous_room.connect_rooms(room, room_direction)

                    # Update iteration variables
                    previous_room = room
                    room_count += 1

                if yy == y:
                    room = Room(room_count, "A Generic Room", "This is a generic room.", column, row)
                    self.grid[y * 2 + 1][max(x, xx) * 2] = room

                    if previous_room is not None:
                        room_direction = self.calculate_room_direction(room, previous_room)
                        previous_room.connect_rooms(room, room_direction)
                    # Update iteration variables
                    previous_room = room
                    room_count += 1
                walk(xx, yy, room_count)
        walk(random.randrange(w), random.randrange(h), room_count)






    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1



    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 44
width = 8
height = 7
# w.generate_rooms(width, height, num_rooms)
w.depth_first_room_generator(width, height)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
