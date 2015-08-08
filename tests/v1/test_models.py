from .test_base import TestBase
from logic.v1.models import Document, db
from logic.v1.core.models import User
from logic.v1.args import Arg, KeyArg


class Sample(Document):
	
	the_choices = Document.choices('a', 'b', 'c')
	
	string = db.StringField()
	email = db.EmailField()
	reference = db.ReferenceField(User)
	choices = db.StringField(choices=the_choices)
	required = db.StringField(required=True)
	default = db.StringField(default=True)


class TestModels(TestBase):
	
	def test_model_CRUD(self):
		"""basic User CRUD operations"""
		n1, n2 = 'yoyo', 'HAH'
		assert User(name=n1).get() is None
		
		user = User(name=n1).put()
		assert User(name=n1).get() is not None
		assert User(name=n2).get() is None
		assert len(User(name=n1).fetch()) is 1
		
		user.load(name=n2).save()
		assert len(User().fetch()) is 1
		assert User().get().name == n2
		assert User(name=n1).get() is None
		assert User(name=n2).get() is not None
		
		user.delete()
		assert User(name=n1).get() is None
		assert User(name=n2).get() is None
		
	def test_fields_to_args_basic(self):
		"""Tests that field_to_args works"""
		args = Sample.fields_to_args()
		
		self.assert_iterables_similar(
			Sample._fields.keys(),
		    args.keys())
		
		for field in ['string', 'email', 'choices', 'required', 'default']:
			assert isinstance(args[field], Arg)
		
		assert isinstance(args['reference'], Arg)
		assert args['required'].required is True
		assert args['default'].default is True
		
		for field in ['string', 'email', 'required']:
			assert args[field].default is None
			
		for field in ['string', 'email', 'default']:
			assert args[field].required is False