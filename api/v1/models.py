import datetime
import importlib
import json
import api
from bson import ObjectId, DBRef
from . import constants, db
from mongoengine import DoesNotExist


class Document(db.Document):
	"""Basic Document class - handles essential, barebones CRUD operations"""

	primary = 'id'
	created_at = db.DateTimeField(default=datetime.datetime.now)
	updated_at = db.DateTimeField(default=datetime.datetime.now)
	meta = dict(abstract=True)

	def __init__(self, *args, **kwargs):
		"""Initializes methods with permissions checks"""
		super().__init__(*args, **kwargs)
		self.objects = self.__class__.objects
	
	@classmethod
	def choices(cls, *args):
		"""Duplicates all entries of an iterable"""
		assert isinstance(args[0], str), 'choices() args must be strings'
		return [(arg, arg) for arg in args]
	
	def load(self, **kwargs):
		"""Loads kwargs into object"""
		[setattr(self, k, v) for k, v in kwargs.items()]
		return self

	def to_dict(self, excludes=['created_at', 'updated_at']):
		"""Converts to dictionary"""
		return {k: v for k, v in json.loads(self.to_json()).items() 
		        if k not in excludes}

	def get(self):
		"""Basic get operation"""
		try:
			return self.objects.get(**self.to_dict())
		except DoesNotExist:
			return None
		
	def fetch(self):
		"""Fetch operation using queries"""
		return self.objects.filter(**self.to_dict()).all()

	def put(self):
		"""Alias for save"""
		return self.save()

	def __str__(self):
		"""String representation using primary field"""
		return str(getattr(self, self.primary))


# TODO(Alvin): store all models in radix tree in __init__.py
def dereference(self):
	"""dereference a DBRef"""
	collection, _id = self._DBRef__collection, self._DBRef__id
	for dir in constants.MODULES:
		mod = importlib.import_module('%s.v1.%s.models' % (api.root, dir))
		for k, v in vars(mod).items():
			if k == collection and hasattr(k, 'objects'):
				return v.objects(id=ObjectId(_id)).get()

DBRef.get = dereference