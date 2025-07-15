from . import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"
