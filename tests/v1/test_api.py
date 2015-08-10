from flask import url_for
from logic.v1.api import need
from tests.v1.test_base import TestBase


class TestAPI(TestBase):
	"""Tests API functions"""
	
	def test_need_works(self):
		"""Simply tests that Need can be instantiated"""
		@need('put')
		def endpoint():
			pass
		
	def test_api_registered(self, app):
		"""Tests that flask url_for works with api"""
		with app.test_request_context('/'):
			assert url_for('v1.user')
			assert url_for('v1.user_path', path='user')