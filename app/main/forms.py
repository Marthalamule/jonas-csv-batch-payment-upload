from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class CSVUploadForm(FlaskForm):
    file = FileField('Upload CSV', validators=[FileRequired()])
    submit = SubmitField('Upload')