from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SelectField, SubmitField
from wtforms.widgets import PasswordInput, SubmitInput
from wtforms.validators import EqualTo, DataRequired, NumberRange

from maze_site_app.database import user_exists
from maze_site_app.colours import Colours
from maze_site_app.maze_utils import MazeTypes


colour_strings_display = [str(colour)[8:].capitalize() for colour in Colours]
colour_strings_backend = [str(colour)[8:] for colour in Colours]
colour_options = list(zip(colour_strings_backend, colour_strings_display))

maze_strings_display = [str(maze)[10:].capitalize() for maze in MazeTypes]
maze_strings_backend = [str(maze)[10:] for maze in MazeTypes]
maze_options = list(zip(maze_strings_backend, maze_strings_display))


class MazeRequestForm(FlaskForm):
    width = IntegerField(
        'Width',
        validators=[NumberRange(min=10, max=200)]
    )
    height = IntegerField(
        'Height',
        validators=[NumberRange(min=10, max=200)]
    )
    maze_type = SelectField(
        'Maze type',
        choices=maze_options, validators=[]
    )
    wall_colour = SelectField(
        'Wall colour',
        choices=colour_options, validators=[]
    )
    path_colour = SelectField(
        'Path colour',
        choices=colour_options,
        validators=[]
    )
    private = BooleanField(
        'Private'
    )
    submit = SubmitField(
        'Generate Maze',
        widget=SubmitInput()
    )

    def validate(self):
        if not super().validate():
            return False
        result = True
        if self.wall_colour.data == self.path_colour.data:
            self.wall_colour.errors.append('Wall and path colours must be different')
            self.path_colour.errors.append('Wall and path colours must be different')
            result = False
        return result


class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired()]
    )
    password = StringField(
        'Password', 
        validators=[DataRequired()], 
        widget=PasswordInput()
    )
    submit = SubmitField(
        'Login', 
        widget=SubmitInput())


class CreateUserForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired()]
    )
    password = StringField(
        'Password', 
        validators=[DataRequired()], 
        widget=PasswordInput()
    )
    password_double_check = StringField(
        'Password', 
        validators=[DataRequired(), EqualTo('password')], 
        widget=PasswordInput()
    )
    submit = SubmitField(
        'Create Account', 
        widget=SubmitInput()
    )
    
    def validate(self):
        print('validating')
        print(self.username.data)
        if not super().validate():
            return False
        result = True
        if user_exists(self.username.data):
            self.username.errors.append('This username is already taken')
            result = False
        if self.password.data != self.password_double_check.data:
            self.password.errors.append('Passwords must be identical')
            self.password_double_check.errors.append('Passwords must be identical')
            result = False
        return result
