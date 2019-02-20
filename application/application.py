#!/usr/local/bin/python3

from flask import Flask, make_response, render_template, redirect, request
import os
import shutil
import sys

from database import MazeDatabase
from forms import MazeRequestForm
from maze_generator import Maze
from secret import secret


app = Flask(__name__)
app.config['SECRET_KEY'] = secret


DEFAULT_MAZE_CREATOR = "joseph"
DEFAULT_MAZE_WIDTH = 100
DEFAULT_MAZE_HEIGHT = 100

DATABASE_NAME = "mazes.db"
MAZES_FOLDER = "static/maze_files"


database = MazeDatabase(DATABASE_NAME)


@app.route('/')
def home_page():
    last_maze = database.get_latest_maze()
    issue = request.cookies.get('issue')
    response = make_response(render_template('homepage.html', title="Generate a maze", maze=last_maze, issue=issue))
    response.set_cookie('issue', '', expires=0)
    return response


@app.route('/generate_maze', methods=['GET', 'POST'])
def generate_maze():
    form = MazeRequestForm()
    if form.validate_on_submit():
        return build_maze(form)
    return render_template('generate.html', title="Generate a maze", form=form)
    

@app.route('/mazes')
def maze_list():
    mazes = database.get_all_mazes()
    return render_template('viewmazes.html', title="View all mazes", mazes=mazes)


@app.route('/mazes/<int:maze_id>')
def view_maze(maze_id):
    try:
        maze = database.get_maze(maze_id)
        return render_template('viewmaze.html', title=f"Viewing maze {maze.id}", maze=maze)
    except ValueError:
        response = make_response(redirect('/'))
        response.set_cookie('issue', f"Maze with Id {maze_id} could not be found")
        return response


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


def build_maze(form_fields):
    width = form_fields.width.data
    height = form_fields.height.data
    creator = form_fields.creator.data

    maze_id = database.new_entry(creator)
    user_maze = Maze(width, height)
    user_maze.output_maze(maze_id)
    return redirect(f'/mazes/{maze_id}')   


def cleanup_maze_storage():
    if os.path.isfile(DATABASE_NAME):
        os.remove(DATABASE_NAME)

    if os.path.isdir(MAZES_FOLDER):
        shutil.rmtree(MAZES_FOLDER)

    os.makedirs(MAZES_FOLDER)


def setup_database():
    cleanup_maze_storage()
    database.setup_tables()
    maze_id = database.new_entry(DEFAULT_MAZE_CREATOR)
    default = Maze(DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT)
    default.output_maze(maze_id)


if __name__ == "__main__":
    setup_database()

    if len(sys.argv) > 1:
        app.run(host="0.0.0.0", port=80)
    else:
        app.run()
