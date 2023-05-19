from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm (FlaskForm):
    name = StringField ('Enter your name' , validators= [DataRequired() , Length (min=2, max=20)])
    email = StringField ('Enter your email', validators= [DataRequired(), Email()])
    password =PasswordField('Create password', validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField("Register Now")

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
        

class LoginForm (FlaskForm):
    email = StringField ('Enter your email', validators= [DataRequired(), Email()])
    password =PasswordField('Enter your password', validators=[DataRequired() ])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")



class UpdateUserForm (FlaskForm):
    name = StringField ('Enter your name' , validators= [DataRequired() , Length (min=2, max=20)])
    email = StringField ('Enter your email', validators= [DataRequired(), Email()])
    user_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField ('Enter your email', validators= [DataRequired(), Email()])
    submit = SubmitField("Send Request")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That email does not exist. ')
        
class ResetPasswordForm(FlaskForm):
    password =PasswordField('New password', validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")