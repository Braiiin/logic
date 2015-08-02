

class APIException(Exception):
	"""Base for all API Exceptions"""
	code = 400
	message = None
	
	def __init__(self, message=None):
		super().__init__(message)
		self.message = self.message or message
	

class MethodDoesNotExist(APIException):
	code = 404
	message = 'Method endpoint does not exist.'
	
	
class MethodNotAllowed(APIException):
	code = 405
	message = 'Request HTTP Method not allowed.'