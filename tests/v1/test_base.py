from logic import create_app


class TestBase:
	"""Base for all tests"""

	def assert_iterables_similar(self, *args):
		"""Asserts iterables have the same elements, maybe in different orders"""
		args = list(map(list, args))
		[i.sort() for i in args]
		one, rest = args[0], args[1:]
		assert all([one == i for i in rest])