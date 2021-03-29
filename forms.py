from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms import SubmitField
from wtforms import BooleanField

from wtforms.validators import DataRequired
from wtforms.validators import Length


class searchFile(FlaskForm):

    search = StringField('Search anything')
    files_button = FileField('Upload file', validators=[FileAllowed(['.txt'])])
    search_button = SubmitField('Search')
    submit_button = SubmitField('Submit')