#!/usr/local/bin/python3

from collections import namedtuple
import sys

from maze_utils import MazeSpec
from routing import setup_app


FileInformation = namedtuple("FileInformation", ["database_name", "mazes_folder"])


DATABASE_NAME = "mazes.db"
MAZES_FOLDER = "static/maze_files"


DEFAULT_MAZE_CREATOR = "joseph"
DEFAULT_MAZE_WIDTH = 40
DEFAULT_MAZE_HEIGHT = 40


DEFAULT_MAZE = MazeSpec(DEFAULT_MAZE_CREATOR, DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT)
FILE_LOCATIONS = FileInformation(DATABASE_NAME, MAZES_FOLDER)

def main():
    reset = "-r" in sys.argv
    app = setup_app(FILE_LOCATIONS, DEFAULT_MAZE, reset)

    if "-i" in sys.argv:
        app.run(host="0.0.0.0", port=80)
    else:
        app.run()


if __name__ == "__main__":
    main()
