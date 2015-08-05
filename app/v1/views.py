"""
To use the API, invoke 
"""

from flask import Blueprint
from .core.api import UserAPI

# setup Blueprint
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')


def register_api(view, endpoint, url):
	"""Adds BaseAPI to application"""
	v1.add_url_rule(url, view_func=view.as_view(endpoint))
	v1.add_url_rule('%s/<path:path>' % url,
	                view_func=view.as_view('%s_path' % endpoint))
	
register_api(UserAPI, 'user', '/user')