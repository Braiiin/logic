import datetime
import importlib
from bson import ObjectId, DBRef
from . import constants, db


class Document(db.Document):

	primary = '_id'
	created_at = db.DateTimeField(default=datetime.datetime.now)
	updated_at = db.DateTimeField(default=datetime.datetime.now)
	meta = dict(abstract=True)

	def __init__(self, *args, **kwargs):
		"""Initializes methods with permissions checks"""
		super().__init__(*args, **kwargs)

	@classmethod
	def choices(cls, *args):
		assert isinstance(args[0], str), 'choices() args must be strings'
		return [(arg, arg) for arg in args]

	def __str__(self):
		return str(getattr(self, self.primary))


# TODO(Alvin): store all models in radix tree in __init__.py
def dereference(self):
	"""dereference a DBRef"""
	collection, _id = self._DBRef__collection, self._DBRef__id
	for dir in constants.MODULES:
		mod = importlib.import_module('app.v1.%s.models' % dir)
		for k, v in vars(mod).items():
			if k == collection and hasattr(k, 'objects'):
				return v.objects(id=ObjectId(_id)).get()

DBRef.get = dereference