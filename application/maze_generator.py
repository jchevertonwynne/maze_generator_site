from abc import abstractmethod
from PIL import Image, ImageDraw
from random import choice, randrange

from colours import Colours, MazeColours


default_colours = MazeColours(Colours.BLACK, Colours.WHITE)


class Tile:
    """Simple tile class that stores its wall state and its position on board
    north and east walls. only 2 required for defining all walls in a maze
    as one cell's top is another's bottom"""

    def __init__(self, x, y):
        self.top = self.right = True
        self.pos = x, y
    

    def __repr__(self):
        return f"Tile{self.pos}"


class Maze:
    """A simple maze generator. Always starts in top left and ends in
    bottom right.
    name: The file name output. Do not include file extension.
    width, height: Self explanatory. Both default to 200."""

    def __init__(self, width=200, height=200, name="default", colours=default_colours):
        self.width = width
        self.height = height
        self.name = name
        self.colours = colours
        self._board = self.setup_board()
    
    
    @abstractmethod
    def process_maze(self):
        pass


    @staticmethod
    def connect_cells(cell1, cell2):
        curr_x, curr_y = cell1.pos
        next_x, next_y = cell2.pos

        if curr_x > next_x:
            cell2.right = False
        elif next_x > curr_x:
            cell1.right = False
        elif curr_y > next_y:
            cell1.top = False
        elif next_y > curr_y:
            cell2.top = False


    def output_maze(self):
        self.process_maze()
        self.save_maze()


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


    def save_maze(self):
        maze = Image.new(
            "RGB", 
            (self.width * 2 + 1, self.height * 2 + 1), 
            self.colours.path_colour.value
        )
        draw = ImageDraw.Draw(maze)

        # bottom wall
        draw.line(
            (0,
            (self.height * 2),
            ((self.width - 1) * 2), 
            (self.height * 2)),
            fill=self.colours.wall_colour.value,
            width=1,
        )

        # left wall
        draw.line(
            (0, 
            0, 
            0, 
            self.height * 2), 
            fill=self.colours.wall_colour.value,
            width=1
        )

        for row in self._board:
            for cell in row:
                x, y = cell.pos
                if cell.top:
                    draw.line(
                        ((x * 2),
                        (y * 2),
                        (x * 2) + 2,
                        (y * 2)), 
                        fill=self.colours.wall_colour.value,
                        width=1
                    )
                if cell.right:
                    draw.line(
                        ((x * 2) + 2,
                        (y * 2),
                        (x * 2) + 2,
                        (y * 2) + 2),
                        fill=self.colours.wall_colour.value,
                        width=1,
                    )

        maze.save(f"static/maze_files/{self.name}.png")


class RecursiveBacktracker(Maze):
    def process_maze(self):
            start = self._board[randrange(self.height)][randrange(self.width)]
            stack = [start]
            visited = {start}
            adjacent_tiles = {start: self.get_adjacent_tiles(start)}

            while stack:
                curr_tile = stack[-1]
                possible_next = [adjacent for adjacent in adjacent_tiles[curr_tile]
                                 if adjacent not in visited]

                if possible_next:
                    next_tile = choice(possible_next)
                    self.connect_cells(curr_tile, next_tile)

                    adjacent_tiles[next_tile] = self.get_adjacent_tiles(next_tile)
                    visited.add(next_tile)
                    stack.append(next_tile)

                else:
                    del stack[-1]


class ParallelOption(Maze):
    def process_maze(self):
            start = self._board[randrange(self.height)][randrange(self.width)]
            options = {start}
            visited = {start}
            adjacent_tiles = {start: self.get_adjacent_tiles(start)}

            while options:
                curr_tile = choice(list(options))
                possible_next = [adjacent for adjacent in adjacent_tiles[curr_tile]
                                if adjacent not in visited]

                if possible_next:
                    next_tile = choice(list(possible_next))
                    self.connect_cells(curr_tile, next_tile)

                    adjacent_tiles[next_tile] = self.get_adjacent_tiles(next_tile)
                    options.add(next_tile)
                    visited.add(next_tile)

                else:
                    options.remove(curr_tile)
