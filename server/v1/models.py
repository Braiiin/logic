from flask.ext.mongoengine import MongoEngine
import datetime
import importlib
from bson import ObjectId, DBRef
from . import constants


db = MongoEngine()


class Document(db.Document):

	primary = '_id'
	created_at = db.DateTimeField(default=datetime.datetime.now)
	updated_at = db.DateTimeField(default=datetime.datetime.now)

	@classmethod
	def choices(cls, *args):
		assert isinstance(args[0], str), 'choices() args must be strings'
		return [(arg, arg) for arg in args]

	def __str__(self):
		return str(getattr(self, self.primary))

	meta = {
		'abstract': True
	}


def setup_models():
	"""Setup models dictionary"""
	models, dirs = {}, constants.MODULES
	for dir in dirs:
		mod = importlib.import_module('server.v1.%s.models' % dir)
		[models.setdefault(k, v) for k, v in vars(mod).items() 
		 if k[0] == k.upper()[0]]
	return models


def dereference(self):
	""" dereference a DBRef """
	collection, _id = self._DBRef__collection, self._DBRef__id
	return models[collection].objects(id=ObjectId(_id)).get()

models = setup_models()
DBRef.get = dereference