from logic.v1.api import BaseAPI, need
from . import models


class UserAPI(BaseAPI):
	"""API for Users"""
	
	model = models.User

	methods = {
		'get': {},
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
		if need is 'put':
			return user.id == obj.id
		return False
	

class SessionAPI(BaseAPI):
	"""API for login sessions"""
	
	model = models.Session
	
	methods = {
		'get': {},
		'post': {
			'args': model.fields_to_args()
		},
		'put': {
			'args': model.fields_to_args()
		}
	}
	
	def can(self, session, user, need):
		"""Required permissions implementation"""
		if need in ['get', 'post']:
			return True
		if need is 'put':
			return user.id == session.user.get().id
		return False