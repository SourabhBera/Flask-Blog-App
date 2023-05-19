import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_user_image(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename )
    
    #Resizing the image to 150x150 pixels
    output_size = (150,150)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    user_email = str(user.email)
    msg = Message()
    msg.subject = "Password Reset Link"
    msg.recipients = [user_email]
    msg.sender = 'username@gmail.com'
    msg.body = f'''To reset your password, visit the following link: {url_for('users.reset_password', user=user, token=token)}'''
    
    mail.send(msg)