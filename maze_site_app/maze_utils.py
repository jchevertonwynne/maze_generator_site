from collections import namedtuple
from enum import Enum

from maze_site_app.maze_generator import RecursiveBacktracker, ParallelOption, Sidewinder


MazeSpec = namedtuple("MazeSpec", ["user", "width", "height"])


class MazeTypes(Enum):
    RECURSIVE = RecursiveBacktracker
    PARALLEL = ParallelOption
    SIDEWINDER = Sidewinder
