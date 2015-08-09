from mongoengine import NotUniqueError
import pytest
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
		u1 = {'email': 'user1@braiiin.com', 'username': 'u1', 'password': 'p1'}
		u2 = {'email': 'user2@braiiin.com', 'username': 'u2', 'password': 'p2'}
		assert User(**u1).get() is None
		
		user = User(**u1).put()
		# assert user.id is not None
		assert User(**u1).get() is not None
		assert User(**u2).get() is None
		assert len(User(**u1).fetch()) is 1
		
		user.load(**u2).put()
		assert len(User().fetch()) is 1
		assert User().get().email == u2['email']
		assert User(**u1).get() is None
		assert User(**u2).get() is not None
		
		user.delete()
		assert User(**u1).get() is None
		assert User(**u2).get() is None
		
	def test_insert_anon_with_unique(self):
		"""Tests inserting on unique fields"""
		anonymous = User(
			email='an@nymo.us',
			username='an',
			password='@'
		).save()
		with pytest.raises(NotUniqueError):
			User(
				email='an@nymo.us',
				username='an',
				password='@'
			).save()  # cannot attempt to save a NEW object
		anonymous.load(username='huehue').save()  # save existing object is OK
		anonymous = User(
			email='an@nymo.us',
			username='an',
			password='huehue'
		).get_or_create()  # for subsequent retrievals, use get_or_create
		assert anonymous is not None
		
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
			
	def test_fields_to_args_override(self):
		"""Tests that kwargs can be overridden for all fields"""
		args = Sample.fields_to_args(override={'required': False})
		
		assert args['required'].required is False
		
	def test_dereferencing(self):
		"""Tests that dbref.get() works"""
		user = User(
			email='an@nymo.us',
			username='an',
			password='@'
		).save()
		user_key = user.to_dbref()
		assert user_key.get() == user