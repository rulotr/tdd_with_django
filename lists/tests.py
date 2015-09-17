from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item,List
#Para ver solo los def de cada clase: grep -E "class|def" lists/tests.py
class HomePageTest(TestCase):
	
	def test_root_url_incia_al_home(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)

	def test_pagina_principal_retorna_un_html_correcto(self):
		request  = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(),expected_html) #decode convierte bytes a cadenas unicodes

	def test_pagina_principal_solo_guarda_items_cuando_es_necesario(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(),0)


class ListAndItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text ="The first (ever) list item"
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text ="Item the second"
		second_item.list = list_
		second_item.save()

		save_list = List.objects.first()
		self.assertEqual(save_list,list_)

		save_items = Item.objects.all()
		self.assertEqual(save_items.count(), 2)

		first_saved_item = save_items[0]
		second_saved_item = save_items[1]
		self.assertEqual(first_saved_item.text, "The first (ever) list item")
		self.assertEqual(first_saved_item.list,list_)
		self.assertEqual(second_saved_item.text, "Item the second")
		self.assertEqual(second_saved_item.list,list_)


class ListViewTest(TestCase):
	def test_usa_lista_plantilla(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response,'list.html')

	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list=list_)
		Item.objects.create(text='itemey 2', list=list_)

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response,'itemey 1')
		self.assertContains(response,'itemey 2') #self.assertContains no necesita contant.decode()

class NewListTest(TestCase):
	def test_pagina_principal_puede_guardar_un_POST_request(self):
		#request = HttpRequest()
		#request.method = 'POST'
		#request.POST['item_text'] = 'A new list item'
		#response = home_page(request)
		self.client.post('/lists/new', data={'item_text':  'A new list item' })
		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_pagina_principal_redirige_despues_de_un_POST(self):
		#request = HttpRequest()
		#request.method = 'POST'
		#request.POST['item_text'] = 'A new list item'

		#response = home_page(request)
		response =self.client.post('/lists/new', data={'item_text':  'A new list item' })
		
		self.assertRedirects(response,'/lists/the-only-list-in-the-world/') # assertRedirects: toma en cuenta la url completa
#Probar los test python manage.py test