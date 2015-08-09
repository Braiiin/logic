import json
from bson import DBRef
from webargs import Arg


def KeyArg(cls, **kwargs):
	"""Web arg for keys"""
	parse_key = lambda key: {'id': key, 'collection': cls.__name__}
	Key = lambda kwargs: DBRef(**kwargs)
	return Arg(Key, use=parse_key, **kwargs)

	
def KeyRepeatedArg(Arg):
	"""web arg for iterable of Keys"""

	
def BooleanArg(Arg, **kwargs):
	"""web arg for booleans"""
	Bool = lambda s: s.lower() == 'true'
	return Arg(Bool, **kwargs)
	

def DateTimeArg():
	"""web arg for dates"""


def JsonArg():
	"""web arg for JSONs"""
	return Arg(json.loads)