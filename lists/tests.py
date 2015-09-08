from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page

class HomePageTest(TestCase):
	def test_root_url_encia_al_home(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)

	def test_pagina_principal_retorna_un_html_correcto(self):
		request  = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(),expected_html) #decode convierte bytes a cadenas unicodes

		

#Probar los test python manage.py test