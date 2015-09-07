from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

class HomePageTest(TestCase):
	def test_root_url_encia_al_home(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)

	def test_pagina_principal_retorna_un_html_correcto(self):
		request  = HttpRequest()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))


#Probar los test python manage.py test