"""
Examples
--------

/api/v1/user/123456789012345678901234
"""

from logic import db, logger
from .core.models import User, anonymous, Session
from flask import request


session = {}


def current_user():
	"""Returns the user performing this API call"""
	token = request.args.get('access_token', None)
	if not token:
		return anonymous
	session = Session(access_token=token).get()
	if not session:
		return anonymous
	user = session.user.get()
	return user or anonymous