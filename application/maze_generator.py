from PIL import Image, ImageDraw
import random


WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)


class Tile:
    """Simple tile class that stores its wall state and its position on board
    north and east walls. only 2 required for defining all walls in a maze
    as one cell's top is another's bottom"""

    def __init__(self, x, y):
        self.top = self.right = True
        self.pos = x, y


class Maze:
    """A simple maze generator. Always starts in top left and ends in
    bottom right.
    name: The file name output. Do not include file extension.
    width, height: Self explanatory. Both default to 200."""

    def __init__(self, width=200, height=200):
        self.width = width
        self.height = height
        self.assert_input_types()
        self._board = self.setup_board()
        print(f"making maze with width {width} and height {height}")
    

    def output_maze(self, name):
        self.process_maze()
        self.save_maze(name)


    def assert_input_types(self):
        if not isinstance(self.height, int) or self.height < 1:
            raise TypeError("height must be an int of size 1 or more")
        if not isinstance(self.width, int) or self.width < 1:
            raise TypeError("width must be an int of size 1 or more")


    def setup_board(self):
        board = [[Tile(x, y) for x in range(self.width)] 
                             for y in range(self.height)]
        board[0][0].top = False
        return board
    

    def get_adjacent_tiles(self, tile):
        x, y = tile.pos
        options = []
        if x > 0:
            options.append(self._board[y][x - 1])
        if x < self.width - 1:
            options.append(self._board[y][x + 1])
        if y > 0:
            options.append(self._board[y - 1][x])
        if y < self.height - 1:
            options.append(self._board[y + 1][x])
        return options


    def process_maze(self):
        start = self._board[0][0]
        stack = [start]
        visited = {start}
        adjacent_tiles = {start: self.get_adjacent_tiles(start)}

        while stack:
            currTile = stack[-1]
            possible_next = [adjacent for adjacent in adjacent_tiles[currTile] if adjacent not in visited]

            if possible_next:
                nextTile = random.choice(possible_next)
                curr_x, curr_y = currTile.pos
                next_x, next_y = nextTile.pos

                if curr_x > next_x:
                    nextTile.right = False
                elif next_x > curr_x:
                    currTile.right = False
                elif curr_y > next_y:
                    currTile.top = False
                elif next_y > curr_y:
                    nextTile.top = False

                adjacent_tiles[nextTile] = self.get_adjacent_tiles(nextTile)
                visited.add(nextTile)
                stack.append(nextTile)

            else:
                del stack[-1]
    

    def save_maze(self, name):
        maze = Image.new(
            "RGB", 
            (self.width * 2 + 1, self.height * 2 + 1), 
            WHITE
        )
        draw = ImageDraw.Draw(maze)

        # bottom wall
        draw.line(
            (0,
            (self.height * 2),
            ((self.width - 1) * 2), 
            (self.height * 2)),
            fill=BLACK,
            width=1,
        )

        # left wall
        draw.line(
            (0, 
            0, 
            0, 
            self.height * 2), 
            fill=BLACK, 
            width=1
        )

        for row in self._board:
            for item in row:
                x, y = item.pos
                if item.top:
                    draw.line(
                        ((x * 2),
                        (y * 2),
                        (x * 2) + 2,
                        (y * 2)), 
                        fill=BLACK, 
                        width=1
                    )
                if item.right:
                    draw.line(
                        ((x * 2) + 2,
                        (y * 2),
                        (x * 2) + 2,
                        (y * 2) + 2),
                        fill=BLACK,
                        width=1,
                    )

        maze.save(f"static/maze_files/{name}.png")
