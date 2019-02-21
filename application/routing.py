from flask import Flask, make_response, render_template, redirect, request
import os
import shutil

from database import MazeDatabase
from forms import MazeRequestForm
from maze_generator import Maze
from secret import secret


def build_maze(form_fields, database):
    width = form_fields.width.data
    height = form_fields.height.data
    creator = form_fields.creator.data

    maze_id = database.new_entry(creator)
    user_maze = Maze(width, height)
    user_maze.output_maze(maze_id)
    return redirect(f'/mazes/{maze_id}')


def cleanup_maze_storage(database_name, mazes_folder):
    if os.path.isfile(database_name):
        os.remove(database_name)

    if os.path.isdir(mazes_folder):
        shutil.rmtree(mazes_folder)

    os.makedirs(mazes_folder)


def setup_database(database, mazes_folder, default_maze):
    cleanup_maze_storage(database.database_name, mazes_folder)
    database.setup_tables()
    maze_id = database.new_entry(default_maze.user)
    default = Maze(default_maze.width, default_maze.height)
    default.output_maze(maze_id)


def setup_app(database_name, mazes_folder, default_maze):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret


    @app.route('/')
    def home_page():
        last_maze = database.get_latest_maze()
        issue = request.cookies.get('issue')
        response = make_response(render_template(
            'homepage.html', title="Generate a maze", maze=last_maze, issue=issue))
        response.set_cookie('issue', '', expires=0)
        return response


    @app.route('/generate_maze', methods=['GET', 'POST'])
    def generate_maze():
        form = MazeRequestForm()
        if form.validate_on_submit():
            return build_maze(form, database)
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
            response.set_cookie(
                'issue', f"Maze with Id {maze_id} could not be found")
            return response


    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html'), 404


    database = MazeDatabase(database_name)
    setup_database(database, mazes_folder, default_maze)

    return app
