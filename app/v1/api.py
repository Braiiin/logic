"""
API for the Braiiin system

Information
-----------
The API should always return a JSON response, no matter the results of an API
method invocation. Dispatch_request will attempt to catch all exceptions, and
package the results into an error response.

Detail
------
The API is only responsible for correcting formats for input, output. It should
not perform business logic.
"""

from . import logger
from bson import ObjectId
from flask import request, jsonify
from flask.views import View
from webargs.flaskparser import FlaskParser
from .exceptions import MethodDoesNotExist, APIException, MethodNotAllowed


parser = FlaskParser()


@parser.error_handler
def handle_bad_request(err):
	"""Special error handling for API"""
	raise APIException(status=422, message=str(err))


class BaseAPI(View):
	"""
	Extendable class for all APIs as Views

	Information
	-----------
	All APIs implement a dictionary of methods, which details all accepted web
	arguments and methods. This API Resource will attempt to instantiate objects
	where applicable.

	Detail
	------
	The methods dictionary consists of method-information, key-value pairs.
	Information then consists of -- at minimum -- a dictionary of webargs.

	APIViews should attempt to catch errors and throw custom exceptions where
	possible.

	All API methods accept:
	- obj: instance of the API's model
	- data: all valid webargs passed in

	Example
	-------
	class CourseAPI(APIView):
		endpoints = {
			# save is not impelemented below, so model.save() invoked
			'save': {
				'args': {
					'title': Arg(str, required=True)  # a webarg
				}
			},
			'get_students': {
				'get': {
					'args': {
						'type': Arg(str)
					}
				}
			}
		}
	"""

	endpoints = {}

	def dispatch_request(self, path=''):
		"""
		Required method for a Flask class-view, returns output

		Detail
		-----------
		Accepts a path that may be in one of three formats:
		id
		method
		id/method

		"""
		response = dict(status=444, message=None, data={})
		try:
			response.update(dict(status=200, data=self._call_method(path)))
		except APIException as e:
			response.update(dict(status=e.status, message=e.message))
		except Exception as e:
			logger.exception(str(e))
			response.update(dict(status=500, message=str(e)))
		except:
			logger.exception('Unknown exception occurred')
			response.update(dict(status=520, message='Unknown exception occurred.'))
		finally:
			return jsonify(response), response['status']
		
	def _get_method(self, path):
		"""Determines format id, method, or id/method and then returns
		oid, method, settings
		"""
		if '/' in path:
			oid, method = path.split('/')
			return oid, method, self.endpoints[method]
		if hasattr(self, path):  # assumes that ID will never be function name
			return None, path, self.endpoints[path]
		if request.method.lower() in self.endpoints.keys():
			return path, request.method.lower(), self.endpoints
		raise MethodDoesNotExist()

	def _get_settings(self, path):
		"""Retrieve method settings"""
		try:
			oid, method, settings = self._get_method(path)
		except KeyError:
			raise MethodDoesNotExist()
		if request.method.lower() not in settings.keys():
			raise MethodNotAllowed()
		settings = settings[request.method.lower()]
		return oid, settings.get('method', method), settings

	def _get_args(self, settings):
		"""Retrieve web arguments"""
		return parser.parse(settings.get('args', {}), request)
	
	def _get_function(self, obj, method):
		"""Lookup function to be called - first search API, then model"""
		if hasattr(self, method):
			return getattr(self, method)
		if hasattr(obj, method):
			return getattr(obj, method)
		if not obj:
			raise MethodDoesNotExist('API call missing an ID - intended?')
		raise MethodDoesNotExist()
	
	def _call_method(self, path):
		"""Invokes method and returns response"""
		oid, method, settings = self._get_settings(path)
		data = self._get_args(settings)
		obj = self.model(id=ObjectId(oid)).get() if oid else None
		function = self._get_function(obj, method)
		return function(obj, data)
	
	@property
	def model(self):
		"""Alerts programmer of unset model"""
		raise NotImplementedError('Each API requires a model')