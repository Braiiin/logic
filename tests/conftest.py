from app import create_app, config
from pymongo import Connection
import pytest


@pytest.fixture(scope='session')
def app():
	"""New app for test mode"""
	app = create_app(config='TestConfig')
	return app


def clear_database():
	"""Clears database"""
	Connection().drop_database(config.TestConfig.MONGODB_DB)
	

app = app()