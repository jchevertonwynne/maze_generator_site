from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from colours import Colours
from common_utils import MazeTypes


colour_strings_display = [str(colour)[8:].capitalize() for colour in Colours]
colour_strings_backend = [str(colour)[8:] for colour in Colours]
colour_options = list(zip(colour_strings_backend, colour_strings_display))

maze_strings_dispay = [str(maze)[10:].capitalize() for maze in MazeTypes]
maze_strings_backend = [str(maze)[10:] for maze in MazeTypes]
maze_options = list(zip(maze_strings_backend, maze_strings_dispay))


class MazeRequestForm(FlaskForm):
    width = IntegerField('Width', validators=[NumberRange(min=10, max=200)])
    height = IntegerField('Height', validators=[NumberRange(min=10, max=200)])
    creator = StringField("Creator", validators=[DataRequired(message="Please enter your name")])
    maze_type = SelectField("Maze type", choices=maze_options, validators=[])
    wall_colour = SelectField("Wall colour", choices=colour_options, validators=[])
    path_colour = SelectField("Path colour", choices=colour_options, validators=[])
    submit = SubmitField('Generate Maze')

    def validate(self):
        if not super().validate():
            return False
        result = True
        if self.wall_colour.data == self.path_colour.data:
            self.wall_colour.errors.append("Wall and path colours must be different")
            self.path_colour.errors.append("Wall and path colours must be different")
            result = False
        return result
