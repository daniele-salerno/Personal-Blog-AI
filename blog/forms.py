from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Mandatory Field!')])
    password = PasswordField('Password', validators=[DataRequired('Mandatory Field!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired('Mandatory Field!'), 
                        Length(min=3, max=120, message="title range from 3 to 120 chars")]
                        )
    description = TextAreaField('Description', 
                                validators=[Length(max=240, message="description no more than 240 chars")]
                        )
    body = TextAreaField('Content', validators=[DataRequired('Mandatory Field!')])
    image = FileField('Cover Post', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Publish Post')




