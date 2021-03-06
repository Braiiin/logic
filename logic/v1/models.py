import datetime
from bson import ObjectId, DBRef
from . import db
from .args import Arg, KeyArg, JsonArg
from logic.v1.exceptions import APIException
from mongoengine import DoesNotExist
from mongoengine.base import get_document


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
    def _field_to_arg(cls, field, override=None, default=False):
        """Converts a single field to an Arg"""
        name = field.__class__.__name__
        _kwargs = {'required': field.required}
        if field.default and default:
            _kwargs['default'] = field.default
        _kwargs.update(override or {})
        if name == 'BooleanField':
            return BooleanArg(**_kwargs)
        if name == 'ReferenceField':
            return KeyArg(field.document_type_obj, **_kwargs)
        if name == 'DictField':
            return JsonArg(**_kwargs)
        if name == 'IntField':
            return Arg(int, **_kwargs)
        return Arg(str, **_kwargs)

    @classmethod
    def fields_to_args(cls, override=None, default=False, exclude=(), **kwargs):
        """Converts fields to webargs"""
        values = {k: cls._field_to_arg(v, override, default) for k, v
                  in cls._fields.items() if k not in exclude}
        values.update(kwargs)
        return values

    def load(self, **kwargs):
        """Loads kwargs into object"""
        [setattr(self, k, v) for k, v in kwargs.items()]
        return self

    def to_dict(self, excluding=True, map=None):
        """Converts to dictionary
        :param excluding: function taking key, value and returning boolean,
        True to exclude the key-value pair
        """
        if excluding is True:
            excluding = lambda k, v: k in ['created_at', 'updated_at'] \
                and hasattr(self, k)
        if not excluding:
            excluding = lambda k, v: False
        if not callable(excluding):
            raise APIException('Excluding must be one of the following types:'
                'boolean, None, or callable')
        _map = {'_id': 'id'}
        _map.update(map or {})
        return {_map.get(k, k): v for k, v in dict(self.to_mongo()).items()
                if not excluding(k, v)}

    def post(self):
        """Create operation"""
        return self.save(force_insert=True)

    def get(self):
        """Basic get operation - does NOT update original object"""
        try:
            return self.objects.get(**self.to_dict())
        except DoesNotExist:
            return None

    def fetch(self):
        """Fetch operation using queries"""
        return self.objects.filter(**self.to_dict()).all()

    def put(self):
        """Alias for save operation"""
        return self.save()

    def get_or_create(self):
        """Get object or create it"""
        obj = self.get()
        return obj if obj else self.save()

    @property
    def filter(self):
        """Filter by primary"""
        primary = getattr(self, '_id', self.primary)
        return {self.primary: primary} if primary else {}

    def delete(self):
        """Check for ID before deleting"""
        if not hasattr(self, 'id') or not self.id:
            raise APIException('Object has no ID. Either "get" before "delete,"'
                               ' or this object does not exist.')
        super(Document, self).delete()

    def __str__(self):
        """String representation using primary field"""
        return str(getattr(self, self.primary))


def dereference(self):
    """dereference a DBRef"""
    collection, _id = self._DBRef__collection, self._DBRef__id
    model = get_document(collection.capitalize())
    return model.objects(id=ObjectId(_id)).get()

DBRef.get = dereference
