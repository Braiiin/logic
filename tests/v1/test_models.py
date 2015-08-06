from .test_base import TestBase
from tests import conftest
from api.v1.core.models import User


class TestModels(TestBase):

	setup_method = lambda self, method: conftest.clear_database()
	
	def test_user_CRUD(self):
		"""basic User CRUD operations"""
		n1, n2 = 'yoyo', 'HAH'
		assert User(name=n1).get() is None
		
		user = User(name=n1).put()
		assert User(name=n1).get() is not None
		assert User(name=n2).get() is None
		assert len(User(name=n1).fetch()) is 1
		
		user.load(name=n2).save()
		assert len(User().fetch()) is 1
		assert User().get().name == n2
		assert User(name=n1).get() is None
		assert User(name=n2).get() is not None
		
		user.delete()
		assert User(name=n1).get() is None
		assert User(name=n2).get() is None