"""
To use the API, invoke 
"""

from flask import Blueprint
from .core.api import UserAPI, SessionAPI

# setup Blueprint
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')


def register_api(view, endpoint):
	"""Adds BaseAPI to application"""
	v1.add_url_rule('/%s' % endpoint, view_func=view.as_view(endpoint))
	v1.add_url_rule('/%s/<path:path>' % endpoint,
	                view_func=view.as_view('%s_path' % endpoint))
	
register_api(UserAPI, 'user')
register_api(SessionAPI, 'session')