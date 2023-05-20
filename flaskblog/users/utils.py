import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    full_link = "http://127.0.0.1:8000" + url_for('users.reset_password', user=user, token=token)
    user_email = str(user.email)
    
    msg = Message()
    msg.subject = "Password Reset Link"
    msg.recipients = [user_email]
    msg.sender = 'username@gmail.com'
    msg.html= f'''
    <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <!-- Latest compiled and minified CSS -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <title>Document</title>
            </head>
            
            <body>
                <h1 style="font-size: 55px; font-family: 'Times New Roman', Times, serif; display: flex;">Bloggers!</h1>
                <div>
                    <h2>To reset your password, 
                    <a href="{ full_link }" class="btn btn-primary" role="button"> Click Here</a>
                    </h2>

                </div>

            </body>
        </html>
    '''


    mail.send(msg)