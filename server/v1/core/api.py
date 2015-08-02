from server.v1.api import BaseAPI
from . import models


class UserAPI(BaseAPI):
	"""API for Users"""
	
	model = models.User

	methods = {
		'get': {

		},
	}
