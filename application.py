#!/usr/local/bin/python3

from maze_site_app import app, db
from maze_site_app.models import Maze, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Maze': Maze, 'User': User}


def main():
    app.run()


if __name__ == "__main__":
    main()

