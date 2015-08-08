from logic.v1.api import need
from tests.v1.test_base import TestBase


class TestAPI(TestBase):
	"""Tests API functions"""
	
	def test_need_works(self):
		"""Simply tests that Need can be instantiated"""
		@need('put')
		def endpoint():
			pass