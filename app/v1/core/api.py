from app.v1.api import BaseAPI
from app.v1.args import *
from . import models


class UserAPI(BaseAPI):
	"""API for Users"""
	
	model = models.User

	methods = {
		'get': {},
		'put': {}
	}

	endpoints = {
		'save': {},
		'fetch': {},
	    'delete': {}
	}
	
	def can(self, obj, user, need):
		"""Required permissions implementation"""
		return True