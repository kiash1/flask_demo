from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app
import json
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
	"""docstring for ClassName"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), unique=True, nullable=False)
	username = db.Column(db.String(50), unique=True, nullable=False)

	@staticmethod
	def json(self):
		return{'email': self.email, 'password': self.password, 'username': self.username}

	@staticmethod
	def add_user(_email, _password, _username):
		new_user = User(email=_email, password=generate_password_hash(_password, method='sha256'), username=_username)
		db.session.add(new_user)
		db.session.commit()

	@staticmethod
	def get_all_users():
		return [User.json(user) for user in User.query.all()]

	def __repr__(self):
		user_object={
			'email' : self.email,
			'password' : self.password,
			'username'	: self.username
		}
		return json.dumps(book_object)