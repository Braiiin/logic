import flask
from logic.v1 import User
from logic.v1.args import Arg, KeyArg, JsonArg
from .test_base import TestBase
from webargs.flaskparser import FlaskParser


parser = FlaskParser()


class TestArgs(TestBase):
	"""Tests that args behave"""
	
	def test_key_arg(self, app):
		"""tests that key args can be dereferenced"""
		user = User(name='wh@tever.com').save()
		with app.test_request_context('/?test=%s' % str(user.id)):
			user_key = parser.parse_arg('test', KeyArg(User), flask.request)
			assert user_key.get() == user

	def test_json_arg(self, app):
		"""tests that JSON web args are converted"""
		with app.test_request_context('/?test={"yo": "a"}'):
			test = parser.parse_arg('test', JsonArg(), flask.request)
			assert isinstance(test, dict)