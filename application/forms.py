from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

class MazeRequestForm(FlaskForm):
    width = IntegerField('Width', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired()])
    creator = StringField("Creator", validators=[DataRequired()])
    submit = SubmitField('Generate Maze')
