from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Register')