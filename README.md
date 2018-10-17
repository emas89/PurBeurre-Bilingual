# PUR BEURRE Web App - English/French

### French language
![Pur Beurre French](https://github.com/emas89/PurBeurre-Bilingual-in-progress...-/blob/master/purbeurre/static/purbeurre/img/fr.png)

### English language
![Pur Beurre English](https://github.com/emas89/PurBeurre-Bilingual-in-progress...-/blob/master/purbeurre/static/purbeurre/img/en.png)

## A nutritional advisor that helps users to eat healthier foods

### Project based on OpenFoodFacts (https://fr.openfoodfacts.org/)
-----------------------------------------------
### Now it supports also english language
Added english language via internationalisation settings by this way:

#### settings.py :
* imported **unittext_lazy** translation method;
* setted **LocaleMiddleware** between CommonMiddleware and SessionMiddleware;
* added supported english language code **'en',_ ('English');**
* added LOCALE_PATHS **local** as a folder where find translations.

#### urls.py :
* imported **i18n_patterns** function;
* divided admin urls from others;
* added language codes in PurBeurre website URLs.

#### views.py :
* imported **unittext_lazy** translation method;
* marked all wanted items to translate;

#### html files :
* imported label tag **{% load i18n %}** to activate translation;
* marked all wanted items by **{% trans "" %}** label tag.

#### create django.po / django.mo files :
* ran `django-admin makemessages -l en` command from application root folder;
* made translations in **django.po** file;
* ran `django-admin compilemessages` command from project root to create optimized **django.mo** file.

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
