from app.v1.api import BaseAPI
from app.v1.args import *
from . import models


class UserAPI(BaseAPI):
	"""API for Users"""
	
	model = models.User

	methods = {
		'get': {
			'args': {
				'name': Arg(str, required=True)
			}
		},
	}
	
	def get(self, obj, data):
		"""Basic get operation"""
		return data