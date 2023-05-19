import os
import secrets
from PIL import Image
from flask import current_app

def save_blog_image(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, 'static/blog_images', picture_filename )
    
    
    image = Image.open(form_picture)
    image.save(picture_path)
    return picture_filename

