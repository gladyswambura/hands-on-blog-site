from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, 
                    ValidationError, BooleanField)
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp
from ..models import User

class SignupForm(FlaskForm):
    first_name = StringField("Your First Name", validators=[InputRequired()])
    last_name = StringField("Your Last Name", validators=[InputRequired()])
    username = StringField("Your Username",validators=[InputRequired(),Length(3, 20, message="Please provide a valid name"),
        Regexp("^[A-Za-z][A-Za-z0-9_.]*$",0,"Usernames must have only letters, " "numbers, dots or underscores",),])
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    confirmpassword = PasswordField("Confirm Password",validators=[InputRequired(),Length(8, 72),
            EqualTo("password", message="Passwords must match !"),])
    submit = SubmitField("Sign Up")