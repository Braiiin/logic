"""

App Factory
-----------

uses config.py configurations for setup

"""
import importlib
import logging

from flask import Flask
from flask_hashing import Hashing
from flask_mongoengine import MongoEngine

# datastore
db = MongoEngine()

# hashing mechanism
hashing = Hashing()

logger = logging.getLogger('API')

root = 'logic'


def create_app(config='DevelopmentConfig', root=_root, **configs):
	"""
	App factory
	:param config: name of Config class from config.py
	"""

	# Create and set app config
	app = Flask(__name__)
	app.config.from_object('%s.config.%s' % (root, config))
	app.config.update(**configs)

	# initialize MongoEngine with app
	db.init_app(app)

	# initialize hashing mechanism
	hashing.init_app(app)

	# Setup blueprints
	def register_blueprints():
		for view in app.config['LIVE']:
			mod = importlib.import_module('%s.%s.views' % (_root, view))
			app.register_blueprint(getattr(mod, view))

	app.register_blueprints = register_blueprints
	app.register_blueprints()

	return app
