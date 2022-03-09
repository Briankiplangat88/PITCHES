from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms import ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
   
    email = StringField('Enter Your Email Address',validators=[DataRequired(),Email()])
    username = StringField('Enter your username',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(), EqualTo('password_confirm',message = 'Passwords must be identical')])
    password_confirm = PasswordField('Confirm Passwords',validators = [DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is already taken')


class LoginForm(FlaskForm):
    email = StringField('Enter Your Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Enter Your Password',validators =[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')