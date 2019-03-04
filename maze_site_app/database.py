from flask_login import current_user
from sqlalchemy import or_

from maze_site_app import db
from maze_site_app.models import Maze, User


def get_latest_maze():
    if current_user.is_authenticated:
        return Maze.query.filter(or_(Maze.private.is_(False), Maze.creator == current_user.username)) \
            .order_by(Maze.maze_id.desc()) \
            .first()
    else:
        return Maze.query.filter(Maze.private.is_(False))\
                         .order_by(Maze.maze_id.desc())\
                         .first()


def get_maze(maze_id):
    maze = Maze.query.get(maze_id)
    if maze is None:
        raise ValueError(f"Maze with id {maze_id} does not exist")
    if maze.private and maze.creator != current_user.username:
        raise ValueError("Maze is private and belongs to another user")
    return maze


def get_all_mazes():
    if current_user.is_authenticated:
        return Maze.query.filter(or_(Maze.private.is_(False), Maze.creator == current_user.username)) \
            .order_by(Maze.maze_id.desc()) \
            .all()
    else:
        return Maze.query.filter(Maze.private.is_(False))\
                         .order_by(Maze.maze_id.desc())\
                         .all()


def add_maze(creator, private=False):
    new_maze = Maze(creator=creator, private=private)
    db.session.add(new_maze)
    db.session.commit()
    return new_maze


def user_has_access(maze_id):
    if not current_user.is_authenticated:
        return False
    maze = get_maze(maze_id)
    return not maze.private or maze.creator == current_user.username


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
