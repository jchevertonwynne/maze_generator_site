#!/usr/local/bin/python3

from collections import namedtuple
import os
from passlib.hash import pbkdf2_sha256
import sqlite3

from maze_site_app.maze_generator import RecursiveBacktracker


Record = namedtuple("Record", ["id", "date", "creator"])


MazeSpec = namedtuple("MazeSpec", ["user", "width", "height"])
default_maze = MazeSpec("joseph", 80, 80)


class MazeDatabase:
    def __init__(self, database_name="maze_site.db", mazes_folder="maze_site_app/static/maze_files", reset=False):
        self.database_name = database_name
        self.mazes_folder = mazes_folder
        if reset:
            print("Resetting database")
            self.setup_database()

    def cleanup_maze_storage(self):
        if os.path.isfile(self.database_name):
            os.remove(self.database_name)

        for image in os.listdir(self.mazes_folder):
            os.remove(f"{self.mazes_folder}/{image}")

    def setup_database(self):
        print("Setting up database")
        self.cleanup_maze_storage()
        self.setup_tables()
        maze_id = self.new_maze_entry(default_maze.user)
        default = RecursiveBacktracker(default_maze.width, default_maze.height, maze_id)
        default.output_maze(self.mazes_folder)

    def setup_tables(self):
        print("Setting up tables")
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE mazes (id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, "
                           "date DATETIME DEFAULT CURRENT_TIMESTAMP, creator TEXT);")
            cursor.execute("CREATE TABLE users (username TEXT UNIQUE PRIMARY KEY, password TEXT);")

    def get_maze(self, maze_id):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            maze_info = cursor.execute(
                "SELECT * FROM mazes WHERE id=?;", (maze_id,)).fetchone()
            if maze_info:
                return Record(*maze_info)
            else:
                raise ValueError("Maze Id does not exist in this database")

    def get_latest_maze(self):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            maze_info = cursor.execute("SELECT * FROM mazes ORDER BY id DESC LIMIT 1;").fetchone()
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
            mazes = cursor.execute("SELECT * FROM mazes ORDER BY id DESC;").fetchall()

            return [Record(*maze) for maze in mazes]

    def new_maze_entry(self, creator):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO mazes (creator) VALUES (?);", (creator,))

            return cursor.lastrowid

    def user_exists(self, username):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            user = cursor.execute("SELECT username FROM users WHERE username = ?;", (username,)).fetchone()

            return user is not None
            
    def new_user_entry(self, username, password):
        with sqlite3.connect(self.database_name) as db:
            hashed_password = pbkdf2_sha256.hash(password, rounds=200000, salt_size=16)

            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) values (?, ?);", (username, hashed_password))

    def user_login(self, username, password):
        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            db_user = cursor.execute("SELECT * FROM users WHERE username = ?;", (username,)).fetchone()

            if db_user is None:
                return False

            _, db_password = db_user
            return pbkdf2_sha256.verify(password, db_password)
