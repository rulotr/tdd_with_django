#from django.test import LiveServerTestCase 
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
import unittest

#Como es un caso de pruebas lo heredamos de unittest.TestCase
class NewVisitorTest(StaticLiveServerTestCase):
	#Se ejecuta antes de iniciar un test
	def setUp(self):
		self.browser = webdriver.Firefox()		
		#self.browser.implicitly_wait(3) #Espera 3 segundos por si la pagina un no se ha cargado

	#Se ejecuta al final del test no importando si hubo errores	
	def tearDown(self):
		self.browser.refresh() #Es necesario en windows por un bug de django
		self.browser.quit()

	#Es recomendable poner los mentodos de ayuda despues del tearDown
	def buscar_una_fila_en_la_lista(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr') # find_element (si no es un solo elemento marca error) find_elements(varios)
		self.assertIn(row_text,[row.text for row in rows])

	def test_puede_comenzar_una_lista_y_recupearlar_despues(self):
		#Edith ha escuchado acerca de una nueva aplicacion de tareas
		#asi que ella visita la pagina
		#self.assertEqual('http://localhost:8000',self.live_server_url)
		self.browser.get(self.live_server_url) #en lugar de localhost:8000 LiveServerTestCase usa el atributo live_server_url 
		#import time
		#time.sleep(10)
		#Ella revisa que el titulo y cabecero
		
		self.assertIn('To-Do',self.browser.title) #Documentacion de los asserts https://docs.python.org/3/library/unittest.html
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		
		self.assertIn('To-Do', header_text)
		#la caja de texto debe tener una invitacion a ingresas una tarea
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)

		# #Digitamos en la caja de texto
		inputbox.send_keys('Buy peacock feathers')

		#Tecleamos enter para se agregue la tarea
		inputbox.send_keys(Keys.ENTER)

		#Al enter, se actualizara la url
		edit_list_url = self.browser.current_url		
		self.assertRegex(edit_list_url,'/lists/.+')
		self.buscar_una_fila_en_la_lista('1: Buy peacock feathers')

		#Agregamos otra tarea que se llamara  "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		#Digitamos en la caja de texto otra tarea
		inputbox.send_keys('Use peacock feathers to make a fly')

		#Tecleamos enter para se agregue la tarea
		inputbox.send_keys(Keys.ENTER)		        

		# Al actualizarse la pagina muestra las tareas ingresadas
		self.buscar_una_fila_en_la_lista('1: Buy peacock feathers')
		self.buscar_una_fila_en_la_lista('2: Use peacock feathers to make a fly')

		## Nueva sesion del navegador para asegurarnos que no hay indormacion de Edith´s
		self.browser.refresh() #Es necesario en windows por un bug de django
		self.browser.quit() 
		self.browser = webdriver.Firefox()

		#Francis visita la pagina principal, no esta firmada Edith
		self.browser.get(self.live_server_url)		
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)				
		self.assertNotIn('make a fly', page_text)				

		#Francis comienza una nueva lista de tareas
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# #Francis obtiene su propia url
		francis_list_url = self.browser.current_url		
		self.assertRegex(francis_list_url,'/lists/.+')
		self.assertNotEqual(francis_list_url,edit_list_url)
		
		#De nuevo que existan tareas de Edith en la lista de Francis
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk',page_text)



		self.fail('Finish the test!') #Se usa para informar que el test termino

	def test_layout_and_styling(self):
		# Edith visita la pagina principal
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1027,768)

		# Ella nota que la caja de texto esta centrada
		inputbox = self.browser.find_element_by_id('id_new_item')
		#inputbox.send_keys('testing\n')
		self.assertAlmostEqual(
				inputbox.location['x'] + inputbox.size['width'] /2,
				512,
				delta=5
			)

# Como estamos lanzando el test desde ./manage.py test functiona_tests ya no necitamos:
#if __name__ == '__main__': #Si este script se ejecuta desde la linea de comandos y no se esta importando
#	unittest.main(warnings='ignore') #Ejecutamos el programa principal de unittest el cual encontrara las clases y metodos
#browser = webdriver.Firefox()
#Ok Revisar la direccion principal

#Ok El titulo y cabecero de la pagina debe de contener el titulo
#assert 'To-Do' in browser.title

#Ok She is invited to enter a to-do item straight away

#Ok She types "Buy peacock feathers" into a text box (Edith's hobby
# is tying fly-fishing lures)

#Ok When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep