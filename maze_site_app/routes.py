from flask import Flask, make_response, render_template, redirect, request, session
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from maze_site_app import app, database
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


@app.route('/')
def home_page():
    last_maze = database.get_latest_maze()
    issue = request.cookies.get('issue')
    response = make_response(render_template('homepage.html', maze=last_maze, issue=issue))
    response.set_cookie('issue', '', expires=0)
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        return verify_login(form, database)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session['username']

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateUserForm(database)
    if request.method == 'POST' and form.validate_on_submit():
        return create_user_account(form, database)
    return render_template('create_account.html', form=form)

@app.route('/generate_maze', methods=['GET', 'POST'])
def generate_maze():
    form = MazeRequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        return build_maze(form, database)
    return render_template('generate.html', form=form)

@app.route('/mazes')
def maze_list():
    mazes = database.get_all_mazes()
    return render_template('viewmazes.html', mazes=mazes)

@app.route('/mazes/<int:maze_id>')
def view_maze(maze_id):
    try:
        maze = database.get_maze(maze_id)
        return render_template('viewmaze.html', maze=maze)
    except ValueError:
        response = make_response(redirect('/'))
        response.set_cookie(
            'issue', f"Maze with Id {maze_id} could not be found")
        return response

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404