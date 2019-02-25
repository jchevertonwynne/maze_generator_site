#!/usr/local/bin/python3

from collections import namedtuple
from glob import glob
import os
import sqlite3

from maze_generator import RecursiveBacktracker


Record = namedtuple("Record", ["id", "date", "creator"])


def setup_database(database, mazes_folder, default_maze):
    cleanup_maze_storage(database.database_name, mazes_folder)
    database.setup_tables()
    maze_id = database.new_entry(default_maze.user)
    default = RecursiveBacktracker(
        default_maze.width, default_maze.height, maze_id)
    default.output_maze()


def cleanup_maze_storage(database_name, mazes_folder):
    if os.path.isfile(database_name):
        os.remove(database_name)
    
    for image in os.listdir(mazes_folder):
        os.remove(f"{mazes_folder}/{image}")


class MazeDatabase:
    def __init__(self, database_name):
        self.database_name = database_name
    

    def setup_tables(self):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE mazes (id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, "
                        "date DATETIME DEFAULT CURRENT_TIMESTAMP, creator TEXT);")


    def get_maze(self, id):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            maze_info = cursor.execute(
                "SELECT * FROM mazes WHERE id=?;", (id,)).fetchone()
            if maze_info:
                return Record(*maze_info)
            else:
                raise ValueError("Maze Id does not exist in this database")


    def get_latest_maze(self):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            maze_info = cursor.execute(
                "SELECT * FROM mazes ORDER BY id DESC LIMIT 1;").fetchone()
            if maze_info:
                return Record(*maze_info)
            else:
                raise ValueError("Maze Id does not exist in this database")


    def mazes_exist(self):
        try:
            self.get_latest_maze()
            return True
        except ValueError:
            return False


    def get_all_mazes(self):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            mazes = cursor.execute(
                "SELECT * FROM mazes ORDER BY id DESC;").fetchall()
            return [Record(*maze) for maze in mazes]


    def new_entry(self, creator):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO mazes (creator) VALUES (?);", (creator,))
            return cursor.lastrowid
