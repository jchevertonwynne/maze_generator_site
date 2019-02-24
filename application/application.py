#!/usr/local/bin/python3

import sys

from maze_utils import MazeSpec
from routing import setup_app


DATABASE_NAME = "mazes.db"
MAZES_FOLDER = "static/maze_files"


DEFAULT_MAZE_CREATOR = "joseph"
DEFAULT_MAZE_WIDTH = 40
DEFAULT_MAZE_HEIGHT = 40


DEFAULT_MAZE = MazeSpec(DEFAULT_MAZE_CREATOR, DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT)


def main():
    app = setup_app(DATABASE_NAME, MAZES_FOLDER, DEFAULT_MAZE)

    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        app.run(host="0.0.0.0", port=80)
    else:
        app.run()


if __name__ == "__main__":
    main()
