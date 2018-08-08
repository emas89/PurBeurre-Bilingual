# PUR BEURRE Web App
## A nutritional advisor that helps users to eat healthier foods

![Pur Beurre Homepage](https://github.com/emas89/Project-8_PurBeurre_webapp/blob/master/purbeurre/static/purbeurre/img/thumb.jpg)

### Project based on OpenFoodFacts (https://fr.openfoodfacts.org/)

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
------------------------------------------------
## 3. Heroku Deployment :
