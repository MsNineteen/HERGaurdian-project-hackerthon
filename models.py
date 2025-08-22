from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))  # URL to image

    def __repr__(self):
        return f'<Testimonial {self.author}>'