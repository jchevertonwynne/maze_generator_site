from collections import namedtuple
from enum import Enum


MazeColours = namedtuple("MazeColours", ["wall_colour", "path_colour"])


class Colours(Enum):
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 128, 0)
    LIME = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    MAROON = (128, 0, 0)
    NAVY = (0, 0, 128)
    OLIVE = (128, 128, 0)
    PINK = (255, 51, 153)
    PURPLE = (128, 0, 128)
    RED = (255, 0, 0)
    TEAL = (0, 128, 128)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
