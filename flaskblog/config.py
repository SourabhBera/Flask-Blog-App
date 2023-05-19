import os

class Config:
    SECRET_KEY = '26af2164b8db1f7b25a30f72c4e8c3b4'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blogapp.db'  
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'blogggers.app@gmail.com'
    MAIL_PASSWORD = 'yymzagfockzhjlxw'
    