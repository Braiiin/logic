from logic import create_app, config, db
from mongoengine.connection import _get_db
import pytest


@pytest.fixture(scope='session')
def app():
	"""New app for test mode"""
	app = create_app(config='TestConfig')
	return app


def clear_database():
	"""Clears database"""
	db = _get_db()
	db.connection.drop_database(config.TestConfig.MONGODB_DB)
	

def clear_models(*models):
	"""Clears a set of collections"""
	assert hasattr(models, '__iter__'), 'Accepts iterable'
	for model in models:
		model.objects.delete()


def pytest_runtest_setup(item):
	"""Setup for each test"""
	clear_database()
	print('setting up', item)

test = app()