from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
import datetime
import jwt
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False )
    password = db.Column(db.String(70), nullable=False)
    user_image = db.Column(db.String(20), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    

    def get_reset_token(self):
        
        
        timer = (datetime.datetime.utcnow()+datetime.timedelta(minutes=1))
        new_timer = timer.strftime("%Y-%m-%d %H:%M:%S")
        timer_serializer = json.dumps(new_timer)
        print("\nThe timer is here!", timer_serializer)

        secret= current_app.config['SECRET_KEY']
        payload = {"user_id": self.id, 'expires': timer_serializer}

        encoded_JWT_token = jwt.encode(payload, secret, algorithm="HS256")
        print("\nGot the encoded JWT token \n")
        return encoded_JWT_token

    
    @staticmethod
    def verify_reset_token(encoded_JWT_token):
        secret= (current_app.config['SECRET_KEY'])

        try:
            decoded_JWT_token = jwt.decode(encoded_JWT_token, secret, algorithms=["HS256"])
            print("\nGot the decoded JWT token \n")
            
        except Exception as e:
            print("Error Occured In JWT token !!", e)

        return User.query.get(decoded_JWT_token['user_id'])


    def __repr__(self):
        return f"User('{self.name}', {self.email}, {self.user_image}, {self.password})"
 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False )
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    blog_image = db.Column(db.String(20), default="https://images.pexels.com/photos/1402787/pexels-photo-1402787.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.title}', {self.date_posted}, {self.blog_image})"

