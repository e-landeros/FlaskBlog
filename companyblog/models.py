from companyblog import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), null=False, default = 'default_profile.png')# will be a link to a user file 
    email = db.Column(db.String(64), unique=True, index=True) # index true allows you to make the column an index to connect to other tables
    username = db.Column(db.String(64), unique=True, index=True)

class BlogPost(db.Model):
    pass