from api.v1.api import BaseAPI, need
from . import models


class UserAPI(BaseAPI):
	"""API for Users"""
	
	model = models.User

	methods = {
		'get': {},
		'post': {},
		'put': {},
		'delete': {}
	}

	endpoints = {
		'fetch': {}
	}
	
	def can(self, obj, user, need):
		"""Required permissions implementation"""
		return True
	

class SessionAPI(BaseAPI):
	"""API for login sessions"""
	
	model = models.Session
	
	methods = {
		'get': {},
	    'post': {},
	    'put': {}
	}
	
	def can(self, obj, user, need):
		"""Required permissions implementation"""
		return True