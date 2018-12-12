from companyblog import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), null=False, default = 'default_profile.png')# will be a link to a user file 
    email = db.Column(db.String(64), unique=True, index=True) # index true allows you to make the column an index to connect to other tables
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username { self.username } "  
    
      
class BlogPost(db.Model):
    pass