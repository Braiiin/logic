"""
Examples
--------

/api/v1/user/123456789012345678901234
"""

from api import db, logger
from .core.models import User, anonymous, Session
from flask import request


def authenticate():
	"""Returns the user performing this API call"""
	token = request.args.get('token', None)
	if not token:
		return anonymous
	session = Session(token=token).get()
	if not session:
		return anonymous
	user = session.user.get()
	return user or anonymous
	
current_user = authenticate()