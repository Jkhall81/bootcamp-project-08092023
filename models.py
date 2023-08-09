from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	name = db.Column(db.String(150))
	bio = db.Column(db.String(150))
	movies = db.relationship('Movie', backref='user', lazy=True)

	def __repr__(self):
		return f'User(name={self.name}, email={self.email}, bio={self.bio})'


class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	director = db.Column(db.String(150))
	year = db.Column(db.Integer)
	plot = db.Column(db.Text)
	rating = db.Column(db.Float)
	poster = db.Column(db.String(300))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'Movie(name={self.name}, director={self.director}, year={self.year})'


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	subject = db.Column(db.Text, nullable=False)
	comment_text = db.Column(db.Text, nullable=False)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

	def __repr__(self):
		return f'Comment(subject={self.subject}, comment_text={self.comment_text}, date_posted={self.date_posted})'
