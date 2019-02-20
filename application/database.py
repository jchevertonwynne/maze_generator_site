#!/usr/local/bin/python3

import sqlite3
import os
import shutil
from collections import namedtuple

from maze_generator import Maze


DATABASE_NAME = "mazes.db"
MAZES_FOLDER = "static/maze_files"

DEFAULT_MAZE_CREATOR = "joseph"
DEFAULT_MAZE_WIDTH = 100
DEFAULT_MAZE_HEIGHT = 100


Record = namedtuple("Record", ["id", "date", "creator"])


def cleanup_maze_storage():
    if os.path.isfile(DATABASE_NAME):
        os.remove(DATABASE_NAME)

    if os.path.isdir(MAZES_FOLDER):
        shutil.rmtree(MAZES_FOLDER)
    
    os.makedirs(MAZES_FOLDER)


def setup_database():
    cleanup_maze_storage()
    default = Maze(DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT)

    with sqlite3.connect(DATABASE_NAME) as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE mazes (id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, "
                        "date DATETIME DEFAULT CURRENT_TIMESTAMP, creator TEXT);")
        maze_id = new_entry(DEFAULT_MAZE_CREATOR)
        default.output_maze(maze_id)


def get_maze(id):
    with sqlite3.connect(DATABASE_NAME) as db:
        cursor = db.cursor()
        maze_info = cursor.execute(
            "SELECT * FROM mazes WHERE id=?;", (id,)).fetchone()
        if maze_info:
            return Record(*maze_info)
        else:
            raise ValueError("Maze Id does not exist in this database")


def get_latest_maze():
    with sqlite3.connect(DATABASE_NAME) as db:
        cursor = db.cursor()
        maze_info = cursor.execute(
            "SELECT * FROM mazes ORDER BY id DESC LIMIT 1;").fetchone()
        return Record(*maze_info)


def get_all_mazes():
    with sqlite3.connect(DATABASE_NAME) as db:
        cursor = db.cursor()
        mazes = cursor.execute(
            "SELECT * FROM mazes ORDER BY id DESC;").fetchall()
        return [Record(*maze) for maze in mazes]


def new_entry(creator):
    with sqlite3.connect(DATABASE_NAME) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO mazes (creator) VALUES (?);", (creator,))
        return cursor.lastrowid


if __name__ == "__main__":
    setup_database()
