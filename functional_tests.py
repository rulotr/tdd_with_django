from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

#Como es un caso de pruebas lo heredamos de unittest.TestCase
class NewVisitorTest(unittest.TestCase):
	#Se ejecuta antes de iniciar un test
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3) #Espera 3 segundos por si la pagina un no se ha cargado

	#Se ejecuta al final del test no importando si hubo errores	
	def tearDown(self):
		self.browser.quit()

	def test_puede_comenzar_una_lista_y_recupearlar_despues(self):
		#Edith ha escuchado acerca de una nueva aplicacion de tareas
		#asi que ella visita la pagina
		self.browser.get('http://localhost:8000')

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

		#Digitamos en la caja de texto
		inputbox.send_keys('Buy peacock feathers')

		#Tecleamos enter para se agregue la tarea
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
				any(row.text == '1:Buy peacock feathers' for row in rows),
				"New to-do item did not appear in table"
		)


		self.fail('Finish the test!') #Se usa para informar que el test termino
	
if __name__ == '__main__': #Si este script se ejecuta desde la linea de comandos y no se esta importando
	unittest.main(warnings='ignore') #Ejecutamos el programa principal de unittest el cual encontrara las clases y metodos
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