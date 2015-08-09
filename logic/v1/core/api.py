import json
from datetime import datetime
from logic import hashing
from logic.v1 import session
from logic.v1.api import BaseAPI, need
from .models import User, Session
from logic.v1.args import KeyArg, Arg


class UserAPI(BaseAPI):
	"""API for Users"""
	
	model = User

	methods = {
		'get': {
			'args': model.fields_to_args(override={'required': False})
		},
		'post': {
			'args': model.fields_to_args()
		},
		'put': {
			'args': model.fields_to_args()	
		},
		'delete': {}
	}

	endpoints = {
		'fetch': {}
	}
	
	def can(self, obj, user, need):
		"""Required permissions implementation"""
		if need in ['post', 'fetch', 'get']:
			return True
		if need == 'put':
			return user.id == obj.id
		return False
	
	def post_get(self, obj, data, rval):
		"""Generates access_token if hashed password found"""
		password, rval.password = rval.password, None
		test_password = data.pop('password', None)
		if password and password == test_password:
				salt = hashing.hash_value(str(datetime.now()))
				access_token = hashing.hash_value(password, salt=salt)
				Session(
					access_token=access_token,
					user=rval).post()
				session['user'] = rval
				# TODO: generalize way of adding data to return value
				rval = json.loads(rval.to_json())
				rval.update({'access_token': access_token})
		return rval
			

class SessionAPI(BaseAPI):
	"""API for login sessions"""
	
	model = Session
	
	methods = {
		'get': {
			'args': model.fields_to_args(override={'required': False})
		},
		'put': {
			'args': model.fields_to_args()
		}
	}
	
	def can(self, session, user, need):
		"""Required permissions implementation"""
		if need in ['get', 'post']:
			return True
		if need == 'put':
			return user.id == session.user.get().id
		return False