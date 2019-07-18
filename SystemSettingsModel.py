from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app
import json

db = SQLAlchemy(app)


class SystemSettings(db.Model):
	"""docstring for ClassName"""
	__tablename__ = 'system_settings'
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.Boolean, nullable=False, default=True)

	@staticmethod
	def json(self):
		return{'id': self.id, 'status': self.status}

	@staticmethod
	def add_system_settings(_status):
		new_settings = SystemSettings(status=_status)
		db.session.add(new_settings)
		db.session.commit()

	@staticmethod
	def update_settings_status(_id, _status):
		status_to_update = SystemSettings.query.filter_by(id=_id).first()
		status_to_update.status = _status
		db.session.commit()

	@staticmethod
	def get_all_settings():
		return SystemSettings.json(SystemSettings.query.first())

	@staticmethod
	def get_all():
		return SystemSettings.query.all()

	def __repr__(self):
		system_settings_object={
			'status' : self.status
		}
		return json.dumps(system_settings_object)