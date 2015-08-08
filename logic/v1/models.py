import datetime
import importlib
import json
import logic
from bson import ObjectId, DBRef
from . import constants, db
from .args import Arg, KeyArg, JsonArg
from logic.v1.exceptions import APIException
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
	
	@classmethod
	def _field_to_arg(cls, field, override=None):
		"""Converts a single field to an Arg"""
		to_arg = {
			'ReferenceField': KeyArg,
		    'DictField': JsonArg,
		}
		to_type = {
			'ReferenceField': getattr(field, 'document_type_obj', None),
			'IntField': int
		}
		name = field.__class__.__name__
		_cls = to_arg.get(name, Arg)
		_type, _kwargs = to_type.get(name, str), {}
		_kwargs['required'] = field.required
		if field.default:
			_kwargs['default'] = field.default
		_kwargs.update(override or {})
		return _cls(_type, **_kwargs)
	
	@classmethod
	def fields_to_args(cls, override=None):
		"""Converts fields to webargs"""
		return {k: cls._field_to_arg(v, override) for k, v in cls._fields.items()}
	
	def load(self, **kwargs):
		"""Loads kwargs into object"""
		[setattr(self, k, v) for k, v in kwargs.items()]
		return self

	def to_dict(self, excludes=['created_at', 'updated_at']):
		"""Converts to dictionary"""
		return {k: v for k, v in json.loads(self.to_json()).items() 
		        if k not in excludes}

	def post(self):
		"""Create operation"""
		return self.save(force_insert=True)

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
		self.save()
	
	def delete(self):
		"""Check for ID before deleting"""
		if not hasattr(self, 'id') or not self.id:
			raise APIException('Object has no ID. Either "get" before "delete,"'
							   ' or this object does not exist.')
		super(Document, self).delete()

	def __str__(self):
		"""String representation using primary field"""
		return str(getattr(self, self.primary))


# TODO(Alvin): store all models in radix tree in __init__.py 
# or find mongoengine dereference
def dereference(self):
	"""dereference a DBRef"""
	collection, _id = self._DBRef__collection, self._DBRef__id
	for dir in constants.MODULES:
		mod = importlib.import_module('%s.v1.%s.models' % (logic.root, dir))
		for k, v in vars(mod).items():
			if k == collection and hasattr(v, 'objects'):
				print(_id)
				return v.objects(id=ObjectId(_id)).get()

DBRef.get = dereference