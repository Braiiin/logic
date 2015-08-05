from .test_base import TestBase
from app.v1.exceptions import *


class TestException(TestBase):
	"""Tests exceptions"""
	
	def test_init_default_message(self):
		"""Tests that an exception can be raised basiaclly"""
		message = 'Cat ipsum love lick.'
		assert APIException(message).message == message
	
	def test_init_override(self):
		"""Tests that passing status, mesasge to init overrides props"""
		status = 888
		assert APIException(status=status).status == status