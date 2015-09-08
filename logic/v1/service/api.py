from logic.v1.api import BaseAPI, need
from .models import Service, Employment, Token


class ServiceAPI(BaseAPI):
    """service API"""

    model = Service

    methods = {
        'get': {
            'args': model.fields_to_args(override={'required': False})
        },
        'post': {
            'args': model.fields_to_args()
        },
        'put': {
            'args': model.fields_to_args()
        },
        'delete': {}
    }

    endpoints = {
        'fetch': {},
        'get_or_create': {
            'args': model.fields_to_args()
        },
    }

    def can(self, obj, user, need):
        """Required permissions implementation"""
        if need in ['post', 'fetch', 'get', 'put']:
            return True
        return False


class EmploymentAPI(BaseAPI):
    """employment API"""

    model = Employment

    methods = {
        'get': {
            'args': model.fields_to_args(override={'required': False})
        },
        'post': {
            'args': model.fields_to_args()
        },
        'put': {
            'args': model.fields_to_args()
        },
        'delete': {}
    }

    endpoints = {
        'fetch': {}
    }

    def can(self, obj, user, need):
        """Required permissions implementation"""
        if need in ['post', 'fetch', 'get', 'put']:
            return True
        return False


class TokenAPI(BaseAPI):
    """token API"""

    model = Token

    methods = {
        'get': {
            'args': model.fields_to_args(override={'required': False})
        },
        'post': {
            'args': model.fields_to_args()
        },
        'put': {
            'args': model.fields_to_args()
        },
        'delete': {}
    }

    endpoints = {
        'fetch': {}
    }

    def can(self, obj, user, need):
        """Required permissions implementation"""
        if need in ['post', 'fetch', 'get', 'put']:
            return True
        return False
