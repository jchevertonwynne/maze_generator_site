from flask import make_response, render_template, redirect, request, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user

from maze_site_app import app
from maze_site_app.database import get_latest_maze, get_all_mazes, get_maze, add_maze, add_user, user_has_access, user_login
from maze_site_app.colours import Colours, MazeColours
from maze_site_app.maze_utils import MazeTypes
from maze_site_app.forms import CreateUserForm, LoginForm, MazeRequestForm


def create_default_maze():
    default_maze = add_maze("default")
    maze = MazeTypes.PARALLEL.value(name=default_maze.maze_id)
    maze.output_maze()
    return default_maze


def generate_maze(form):
    creator = current_user.username
    width = form.width.data
    height = form.height.data
    maze_type = form.maze_type.data
    wall_colour = form.wall_colour.data
    path_colour = form.path_colour.data
    private = form.private.data

    new_maze = add_maze(creator, private)
    maze_id = new_maze.maze_id
    maze_generation_type = MazeTypes[maze_type].value
    maze_colours = MazeColours(Colours[wall_colour], Colours[path_colour])
    user_maze = maze_generation_type(width, height, maze_id, maze_colours)
    user_maze.output_maze()
    return redirect(f'/mazes/{maze_id}')


def create_account(form):
    username = form.username.data
    password = form.password.data
    user = add_user(username, password)
    login_user(user)
    return redirect('/')


def login(form):
    username = form.username.data
    password = form.password.data
    try:
        login_user(user_login(username, password))
        next_page = request.args.get('next')
        if next_page is None:
            return redirect('/')
        return redirect(next_page)
    except ValueError:
        return render_template('login.html', form=form)


def serve_maze(maze_id):
    if user_has_access(maze_id):
        return send_from_directory('protected/maze_files', f'{maze_id}.png')
    else:
        raise ValueError('Access to maze not permitted')


@app.route('/')
def home_page_route():
    last_maze = get_latest_maze()
    if last_maze is None:
        last_maze = create_default_maze()
    issue = request.cookies.get('issue')
    response = make_response(render_template('homepage.html', maze=last_maze, issue=issue))
    response.set_cookie('issue', '', expires=0)
    return response


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    form = LoginForm()
    if current_user.is_authenticated:
        redirect('/')
    if request.method == 'POST' and form.validate_on_submit():
        return login(form)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_route():
    logout_user()
    return redirect('/')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account_route():
    form = CreateUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        return create_account(form)
    return render_template('create_account.html', form=form)


@app.route('/generate_maze', methods=['GET', 'POST'])
@login_required
def generate_maze_route():
    form = MazeRequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        return generate_maze(form)
    return render_template('generate.html', form=form)


@app.route('/mazes')
def maze_list_route():
    mazes = get_all_mazes()
    return render_template('viewmazes.html', mazes=mazes)


@app.route('/mazes/<int:maze_id>')
def view_maze_route(maze_id):
    try:
        maze = get_maze(maze_id)
        return render_template('viewmaze.html', maze=maze)
    except ValueError:
        response = make_response(redirect('/'))
        response.set_cookie('issue', f'Maze with Id {maze_id} could not be found')
        return response


@app.route('/protected/<int:maze_id>')
def serve_image_route(maze_id):
    try:
        return serve_maze(maze_id)
    except ValueError:
        response = make_response(redirect('/'))
        response.set_cookie('issue', f'Maze with Id {maze_id} could not be found')
        return response


@app.errorhandler(404)
def not_found_route(error):
    return render_template('error.html', error=error), 404
