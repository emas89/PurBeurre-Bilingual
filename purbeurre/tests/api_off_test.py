# Imports
import json
from purbeurre.models import Categories, Products
from purbeurre.management.commands.api_off import Command
from django.test import TestCase


# api_off command
class CommandTestCase(TestCase):
	"""
	Tests the api_off command that updates the database
	"""
	def setUp(self):
		"""
		Limit to one category to explore
		"""
		self.com = Command()
		self.category = "Fromages"
		prod_data = {
			"product_name": "Comté",
			"product_id": 123,
			"product_url": "http://",
			"product_img": "http://",
			"nutriscore": "c",
			"fat": 6.3,
			"saturated_fat": 1,
			"salt": 0.1,
			"sugar": 13,
			"categories": ['en:plant-based-foods-and-beverages']
			}
		self.content = [prod_data]

	def test_handle(self):
		json_results = open("purbeurre/tests/mockup/off.json")
		mock = json.load(json_results)

		def mockreturn(a):
			return mock

		# Execute the command
		self.com._request_api = mockreturn
		self.com.handle()

		# The DB must have been populated
		self.assertEqual(Products.objects.all().exists(), True)
		self.assertEqual(Categories.objects.all().exists(), True)