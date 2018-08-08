""" 
Script to populate and update PurBeurre database with
OpenFoodFactsdata in JSON extension via his API
"""

# ----------------------------------------------------------------------------------------------------------
# To run this script run "manage.py api_off" command in your console.
# ----------------------------------------------------------------------------------------------------------


# Imports
import requests
from django.core.management.base import BaseCommand
from purbeurre.models import Categories, Products
from django.db import IntegrityError


# Command
class Command(BaseCommand):
    """
    Class to handle the "manage.py api_off" command.
    This class updates the DB with the latest info from OFF.
    """

    help = "Use this script to update the database from OpenFoodFacts"

    def handle(self, *args, **kwargs):
        """
        Handle updating process
        """

        # Gives infos about updating process
        self.stdout.write("Updating PurBeurre database...", ending='\n')

        # Considered categories (according to OFF documentation)
        categories = [
            "Biscuits et gâteaux",
            "Desserts",
            "Confitures",
            "Pizzas",
            "Pâtes à tartiner",
            "Céréales et pommes de terre",
            "Boissons",
            "Produits laitiers",
            "Viandes",
            "Produits à tartiner",
            "Petit-déjeuners",
            "Charcuteries",
            "Chocolats",
            "Poissons",
            "Jambons"
        ]

        # For each category
        for category in categories:
            # insert them in DB
            products = self._request_api(category)
            self._insert(products)

    def _request_api(self, category):
        """
        Calls OpenFoodFacts API to get info
        Filters OpenFoodFacts API results
        """

        api_url = "https://fr.openfoodfacts.org/cgi/search.pl"

        # Used parameters
        params = {
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category,
            'action': 'process',
            'json': '1',
            'page_size': '250'
        }

        # Request
        try:
            products_data = requests.get(api_url, params=params)
            products_data = products_data.json()

            i = 0
            content = []
            # Filter data by their nutritional score
            for product in products_data["products"]:
                nutrichar = ['a','b','c','d','e']
                # Ensure that nutriscore have correct value
                if str(*products_data["products"][i]["nutrition_grades_tags"]) in nutrichar:
                    try:
                        extract_data= {
                            "product_name": products_data["products"][i]["product_name"],
                            "product_id": int(products_data["products"][i]["_id"]),
                            "product_url": products_data["products"][i]["url"],
                            "product_img": products_data["products"][i]["image_small_url"],
                            "nutriscore": str(*products_data["products"][i]["nutrition_grades_tags"]),
                            "fat": products_data["products"][i]["nutriments"]["fat_100g"],
                            "saturated_fat": products_data["products"][i]["nutriments"]["saturated-fat_100g"],
                            "salt": products_data["products"][i]["nutriments"]["salt_100g"],
                            "sugar": products_data["products"][i]["nutriments"]["sugars_100g"],
                            "categories": products_data["products"][i]["categories"].split(',')[:1]
                            }
                        content.append(extract_data)
                    except KeyError:
                        pass
                i += 1
            return content

        except requests.exceptions.ConnectionError:
            print("You must be connected in order to create or update the database")

    def _insert(self, prod_data):
        """
        Inserts filtered data in DB
        """
        for prod in prod_data:

            # Fill Categories table with OFF data or create new ones if necessary
            try:
                cat, created = Categories.objects.get_or_create(
                    category_name=prod["categories"]
                    )

                # Fill Products table with OFF data or create new ones if necessary
                Products.objects.update_or_create(
                    id_product=prod["product_id"],
                    product_name=prod["product_name"],
                    url=prod["product_url"],
                    img=prod["product_img"],
                    nutriscore=prod["nutriscore"],
                    fat=prod["fat"],
                    saturated_fat=prod["saturated_fat"],
                    salt=prod["salt"],
                    sugar=prod["sugar"],
                    category=cat
                )
            # Ignore duplicate value
            except IntegrityError:
                continue