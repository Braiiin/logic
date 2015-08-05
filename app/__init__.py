"""

App Factory
-----------

uses config.py configurations for setup

"""
import importlib
import logging

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_kvsession import KVSessionExtension
from simplekv.db.mongo import MongoStore
from simplekv import KeyValueStore

# datastore
db = MongoEngine()

# server-side session
session = KeyValueStore()
kv_session = KVSessionExtension()

# login-management
login_manager = LoginManager()
bcrypt = Bcrypt()

logger = logging.getLogger('API')


def create_app(config='DevelopmentConfig', **configs):
	"""
	App factory
	:param config: name of Config class from config.py
	"""

	# Create and set app config
	app = Flask(__name__)
	app.config.from_object('app.config.%s' % config)
	app.config.update(**configs)
	
	# initialize MongoEngine with app
	db.init_app(app)
	store = MongoStore(
		getattr(db.connection, app.config['MONGODB_DB']),
		app.config['SESSION_STORE'])
	
	# Substitute client-side with server-side sessions
	kv_session.init_app(app, store)
	
	# initialize Flask-Login with app
	login_manager.init_app(app)
	
	# initialize encryption mechanism
	bcrypt.init_app(app)
	
	# register all blueprints
	for view in app.config['LIVE']:
		mod = importlib.import_module('app.{mod}.views'.format(mod=view))
		app.register_blueprint(getattr(mod, view))
	
	return app