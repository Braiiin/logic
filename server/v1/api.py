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

import json
from bson import ObjectId
from flask import request
from flask.views import View
from webargs.flaskparser import FlaskParser
from .exceptions import MethodDoesNotExist, APIException, MethodNotAllowed


def jsonify(obj):
	"""Converts object to valid JSON string"""
	try:
		return json.dumps(obj)
	except TypeError:
		if hasattr(obj, 'to_json'):
			return jsonify(obj.to_json())
		if hasattr(obj, 'items') and callable(obj.items):
			return jsonify({k: jsonify(v) for k, v in obj.items()})
		if hasattr(obj, '__iter__'):
			return jsonify([jsonify(e) for e in obj])


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
		methods = {
			# save is not impelemented below, so model.save() invoked
			'save': {
				'args': {
					'title': Arg(str, required=True)  # a webarg
				}
			},
			'get_students': {
				'get': {
					'type': Arg(str)
				}
			}
		}
	"""

	model = None

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
		response = dict(code=444, message='No response')
		try:
			response = self._call_method(path)
		except APIException as e:
			response = dict(code=e.code, message=e.message)
		except Exception as e:
			response = dict(code=500, message=str(e))
		except:
			response = dict(code=520, message='Unknown exception occurred.')
		finally:
			return jsonify(response)
		
	def _get_method(self, path):
		"""Determines format id, method, or id/method and then returns
		oid, method, settings
		"""
		if '/' in path:
			oid, method = path.split('/')
			return oid, method, self.methods[method]
		if hasattr(self, path):  # assumes that ID will never be function name
			return None, path, self.methods[path]
		if len(path) is not 24:  # rudimentary check for ObjectId
			raise MethodDoesNotExist()
		return path, request.method.lower(), self.methods

	def _get_settings(self, path):
		"""Retrieve method settings"""
		try:
			oid, method, settings = self._get_method(path)
		except KeyError:
			raise MethodDoesNotExist()
		if request.method.lower() not in settings.keys():
			raise MethodNotAllowed()
		return oid, method, settings[request.method.lower()]

	def _get_args(self, settings):
		"""Retrieve web arguments"""
		return FlaskParser().parse(settings.get('args', {}), request)

	def _get_function(self, obj, method):
		"""
		Lookup function to be called

		Information
		-----------
		API methods take precedence; if the method does not exist, BaseAPI will
		attempt to invoke the method with the model. Note that model methods not
		registered with the API cannot be called.
		"""
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