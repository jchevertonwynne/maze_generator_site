from flask import Flask, make_response, render_template, redirect, request
import os
import shutil

from colours import Colours, MazeColours
from common_utils import MazeTypes
from database import MazeDatabase, setup_database
from forms import MazeRequestForm
from secret import secret


def build_maze(form_fields, database):
    width = form_fields.width.data
    height = form_fields.height.data
    creator = form_fields.creator.data
    maze_type = form_fields.maze_type.data
    wall_colour = form_fields.wall_colour.data
    path_colour = form_fields.path_colour.data
    
    maze_generation_type = MazeTypes[maze_type].value
    maze_colours = MazeColours(Colours[wall_colour], Colours[path_colour])

    maze_id = database.new_entry(creator)
    user_maze = maze_generation_type(width, height, maze_id, maze_colours)
    user_maze.output_maze()

    return redirect(f'/mazes/{maze_id}')


def setup_app(database_name, mazes_folder, default_maze):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret


    @app.route('/')
    def home_page():
        last_maze = database.get_latest_maze()
        issue = request.cookies.get('issue')
        response = make_response(render_template(
            'homepage.html', maze=last_maze, issue=issue))
        response.set_cookie('issue', '', expires=0)
        return response


    @app.route('/generate_maze', methods=['GET', 'POST'])
    def generate_maze():
        form = MazeRequestForm()
        if form.validate_on_submit():
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
        return render_template('error.html'), 404


    database = MazeDatabase(database_name)
    setup_database(database, mazes_folder, default_maze)

    return app
