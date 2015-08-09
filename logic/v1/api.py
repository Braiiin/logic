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

from . import logger, session, current_user
import functools
from bson import ObjectId
from flask import request, jsonify
from flask.views import View
from webargs.flaskparser import FlaskParser
from .exceptions import MethodDoesNotExist, APIException, MethodNotAllowed, \
	PermissionError


parser = FlaskParser()


@parser.error_handler
def handle_bad_request(err):
	"""Special error handling for API"""
	raise APIException(status=422, message=str(err))


def need(*needs):
	"""Decorator for endpoints, checks for needs"""
	isstr = lambda s: isinstance(s, str)
	assert hasattr(needs, '__iter__') and all(map(isstr, needs)), \
		'Need must be string(s)'
	
	def decorator(f):
		@functools.wraps(f)
		def helper(self, obj, data):
			violations = [not self.can(obj, session['user'], n) for n in needs]
			if any(violations):
				raise PermissionError()
			return f(self, obj, data)
		return helper
	return decorator


def hook(f):
	"""Decorator for all endpoints, to check for hooks"""
	def call_hook(prefix, self, obj, data, rval=None):
		"""Calls hook if exists"""
		attr = getattr(self, '%s%s' % (prefix, f.__name__), None)
		if callable(attr):
			return attr(obj, data, rval)
		return rval
	
	@functools.wraps(f)
	def helper(self, obj, data):
		call_hook('pre_', self, obj, data)
		rval = f(self, obj, data)
		rval = call_hook('post_', self, obj, data, rval)
		return rval
	return helper


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
			'get': {
				'args': {
					'query': Arg(str, required=True)
				}
			}
		}
	
		endpoints = {
			# save is not impelemented below, so model.save() invoked
			'save': {
				'methods': {'put'},
				'args': {
					'title': Arg(str, required=True)  # a webarg
				}
			},
			'get_students': {
				# methods are by default = {'get'}
				'args': {
					'type': Arg(str)
				}
			}
		}
	"""

	methods = {
		'get': {},
	    'post': {},
	    'put': {},
	    'delete': {}
	}

	endpoints = {
		'fetch': {}
	}
	
	# Functionality

	def dispatch_request(self, path=''):
		"""
		Required method for a Flask class-view, returns output

		Detail
		-----------
		Accepts a path that may be in one of three formats: id, method, or id/method
		"""
		response = dict(status=444, message='No response', data={})
		try:
			session['user'] = current_user()
			response.update(dict(
				status=200, 
				message='Success', 
				data=self._call_method(path)))
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

	def _call_method(self, path):
		"""Invokes method and returns response"""
		oid, method, settings = self._get_settings(path)
		data = self._get_args(settings)
		obj = self.model.objects(id=ObjectId(oid)).get() if oid else None
		function = self._get_function(obj, method)
		return function(obj, data)	

	def _get_settings(self, path):
		"""Retrieve method settings"""
		try:
			oid, function, settings, methods = self._get_method(path)
		except KeyError:
			raise MethodDoesNotExist()
		if request.method.lower() not in methods:
			raise MethodNotAllowed()
		return oid, function, settings
	
	def _get_method(self, path):
		"""Determines format id, method, or id/method and then returns
		oid, method, settings, allowed_methods
		"""
		oid, function, method = None, path, request.method.lower()
		if ObjectId.is_valid(path) or not path:
			return path, method, self.methods[method], self.methods.keys()
		if '/' in path:
			oid, function = path.split('/')
		settings = self.endpoints[function]
		return oid, function, settings, settings.get('methods', {'get'})

	def _get_args(self, settings):
		"""Retrieve web arguments"""
		return parser.parse(settings.get('args', {}), request)
	
	def _get_function(self, obj, method):
		"""Lookup function to be called - first search API, then model"""
		if hasattr(self, method):
			return getattr(self, method)
		if hasattr(obj, method):
			return getattr(obj, method)
		raise MethodDoesNotExist('Endpoint is registered but is missing.')
	
	# Required attributes
	
	@property
	def model(self):
		"""API corresponding model"""
		raise NotImplementedError()
	
	# Required methods
	
	def can(self, obj, user, permission):
		"""Permissions checking for objects, returns boolean"""
		raise NotImplementedError()
	
	# Default endpoints

	@hook
	@need('get')
	def get(self, obj, data):
		"""Basic get operation for current object, allows API call to include
		an ID or object parameters. If an ID is specified, object parameters
		are ignored."""
		return obj or self.model(**data).get()
	
	@hook
	@need('get')
	def fetch(self, _, data):
		"""Fetch multiple objects"""
		return self.model(**data).fetch()
	
	@hook
	@need('post')
	def post(self, obj, data):
		"""Create"""
		assert not None, 'Post creates a new object.'
		return self.model(**data).put()

	@hook
	@need('put')
	def put(self, obj, data):
		"""Update"""
		assert obj is not None, 'ObjectID does not belong to an object.'
		return obj.load(**data).save()
	
	@hook
	@need('delete')
	def delete(self, obj, _):
		"""Basic delete operation for current object"""
		assert obj is not None, 'No such object.'
		return obj.delete()