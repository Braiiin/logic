from flask import Blueprint

# setup Blueprint
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')


def register_api(view, endpoint,  url):
	pass


