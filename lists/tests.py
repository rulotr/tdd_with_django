from django.test import TestCase

class SmokeTest(TestCase):

	def test_bad_math(self):
		self.assertEqueal(1 + 1, 3 )