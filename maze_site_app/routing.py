from flask import Flask, make_response, render_template, redirect, request, session
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from maze_site_app.colours import Colours, MazeColours
from maze_site_app.maze_utils import MazeTypes
from maze_site_app.database import MazeDatabase
from maze_site_app.forms import CreateUserForm, LoginForm, MazeRequestForm


def build_maze(form_fields, database, mazes_folder="maze_site_app/static/maze_files"):
    width = form_fields.width.data
    height = form_fields.height.data
    creator = form_fields.creator.data
    maze_type = form_fields.maze_type.data
    wall_colour = form_fields.wall_colour.data
    path_colour = form_fields.path_colour.data
    
    maze_generation_type = MazeTypes[maze_type].value
    maze_colours = MazeColours(Colours[wall_colour], Colours[path_colour])

    maze_id = database.new_maze_entry(creator)
    user_maze = maze_generation_type(width, height, maze_id, maze_colours)
    user_maze.output_maze(mazes_folder)

    return redirect(f'/mazes/{maze_id}')


def verify_login(form_fields, database):
    username = form_fields.username.data
    password = form_fields.password.data
    if database.user_login(username, password):
        session['username'] = username
        return "this worked!"
    else:
        return "this failed"


def create_user_account(form_fields, database):
    print("Creating user")
    username = form_fields.username.data
    password = form_fields.password.data
    database.new_user_entry(username, password)
    return "user made"


def setup_app(secret, reset=False):
    app = Flask(__name__)

    login = login_manager(app)
    database = MazeDatabase(reset=reset)




    return app
