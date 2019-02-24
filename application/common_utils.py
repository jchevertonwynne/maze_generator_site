from collections import namedtuple
from enum import Enum

from maze_generator import RecursiveBacktracker, ParallelOption


MazeSpec = namedtuple("MazeSpec", ["user", "width", "height"])
Record = namedtuple("Record", ["id", "date", "creator"])


class MazeTypes(Enum):
    RECURSIVE = RecursiveBacktracker
    PARALLEL = ParallelOption
