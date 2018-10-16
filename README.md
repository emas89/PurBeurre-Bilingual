# PUR BEURRE Web App
## A nutritional advisor that helps users to eat healthier foods

### Project based on OpenFoodFacts (https://fr.openfoodfacts.org/)
### Now it supports english language

# Setup
-----------------------------------------------
## 1. Requirements :
* Python 3.x
* Django 2.0.7
* **pip** package management system
* PostgreSQL
* Using a virtual environment is highly recommended
* Dependencies in **requirements.txt** (use `pip install -r requirements.txt` to install them)
------------------------------------------------
## 2. Database :
* PostgreSQL because of project's hosting on Heroku
* **DB's structure implementation** : use `manage.py migrate` command
* **DB update** : use `manage.py api_off` command to populate it with latest using OpenFoodfacts API
