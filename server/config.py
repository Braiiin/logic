"""

Configurations
--------------

Various setups for different app instances

"""


class Config:
	"""Default config"""
	
	DEBUG = False
	TESTING = False
	PORT = 8000
	HOST = '127.0.0.1'
	SCHEME = 'http'
	SECRET_KEY = 'flask+mongoengine=<3'
	STATIC_PATH = 'static'
	SESSION_STORE = 'session'
	MONGODB_DB = 'default'
	LIVE = ['v1']
	
	
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