from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, StopValidation


class IntegerRequired(DataRequired):
    def __call__(self, form, field):
        if not field.data or isinstance(field.data, str) and not field.data.strip() or field.data < 10 or field.data > 200:
            message = field.gettext('This field only alllows integer values from 10 to 200')
            field.errors[:] = []
            raise StopValidation(message)


class MazeRequestForm(FlaskForm):
    width = IntegerField('Width', validators=[IntegerRequired()])
    height = IntegerField('Height', validators=[IntegerRequired()])
    creator = StringField("Creator", validators=[DataRequired(message="Please enter your name")])
    submit = SubmitField('Generate Maze')
