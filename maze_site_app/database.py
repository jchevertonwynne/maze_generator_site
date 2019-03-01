from maze_site_app import db
from maze_site_app.models import Maze, User


def get_latest_maze():
    return Maze.query.order_by(Maze.maze_id.desc()).first()


def get_maze(maze_id):
    maze = Maze.query.get(maze_id)
    if maze is None:
        raise ValueError(f"Maze with id {maze_id} does not exist")
    return maze


def get_all_mazes():
    return Maze.query.order_by(Maze.maze_id.desc()).all()


def add_maze(creator, private=False):
    new_maze = Maze(creator=creator, private=private)
    db.session.add(new_maze)
    db.session.commit()
    return new_maze


def user_exists(username):
    return User.query.get(username) is not None


def add_user(username, password):
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def user_login(username, password):
    if user_exists(username):
        db_user = User.query.get(username)
        if db_user.check_password(password):
            return db_user
    return False
