from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flaskblog.models import User

class NewBlogForm (FlaskForm):
    title = StringField('Enter Blog Title' , validators= [DataRequired()])
    content =TextAreaField('Enter Blog Content', validators=[DataRequired()])
    blog_image = FileField('Blog Picture', validators=[FileAllowed(['jpg', 'png'])])
    encoded_blog_image = StringField('Blog Picture')
    submit = SubmitField("Post New Blog")

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        

class UpdateBlogForm (FlaskForm):
    title = StringField ('Enter Blog Title' , validators= [DataRequired()])
    content =TextAreaField('Enter Blog Content', validators=[DataRequired()])
    blog_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update Blog")
