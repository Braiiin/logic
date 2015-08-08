"""

Configurations
--------------

Various setups for different app instances

"""


class Config:
	"""Default config"""

	DEBUG = False
	TESTING = False
	SESSION_STORE = 'session'
	MONGODB_DB = 'default'
	SECRET_KEY = 'flask+mongoengine=<3'
	LIVE = ['v1']
	STATIC_PATH = 'static'
	
	INIT = {
		'port': 8001,
		'host': '127.0.0.1',
	}
	
	
class ProductionConfig(Config):
	"""Production vars"""
	pass


class DevelopmentConfig(Config):
	"""For local runs"""
	DEBUG = True
	MONGODB_DB = 'dev'
	
	
class TestConfig(Config):
	"""For automated testing"""
	TESTING = True
	MONGODB_DB = 'test'