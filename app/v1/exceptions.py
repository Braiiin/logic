from . import logger


class APIException(Exception):
	"""Base for all API Exceptions"""
	status = 400
	message = None
	
	def __init__(self, message=None, status=None):
		super().__init__(message)
		logger.exception(message)
		self.message = message or self.message
		self.status = status or self.status
	

class MethodDoesNotExist(APIException):
	status = 404
	message = 'Method endpoint does not exist.'
	
	
class MethodNotAllowed(APIException):
	status = 405
	message = 'Request HTTP Method not allowed.'