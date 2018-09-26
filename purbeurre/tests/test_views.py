# Imports
from django.test import TestCase, Client
from django.urls import reverse
from purbeurre.models import Products, Categories, Substitutes, User
from purbeurre.forms import UserCreationForm


# Test: homepage
class IndexPageTestCase(TestCase):
	"""
	Homepage test
	"""
	def test_index_page(self):
		"""
		If returns a http code 200 is ok
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)


# Legals test
class LegalsPageTestCase(TestCase):
	"""
	Legal mentions page test
	"""
	def test_legals_page(self):
		"""
		If returns a http code 200 is ok
		"""
		response = self.client.get(reverse('purbeurre:legals'))
		self.assertEqual(response.status_code, 200)


# Contacts page
class ContactsPageTestCase(TestCase):
	"""
	Contacts page test
	"""
	def test_contacts_page(self):
		"""
		If returns a http code 200 is ok
		"""
		response = self.client.get(reverse('purbeurre:contacts'))
		self.assertEqual(response.status_code, 200)


# Product's details page
class DetailPageTestCase(TestCase):
	"""
	Product's details page test
	"""
	def setUp(self):
		"""
		Food data
		"""
		category = Categories.objects.create(category_name="Pâte à tartiner")
		nutella = Products.objects.create(
			id_product=1,
			product_name="nutella",
			category=category
			)
		self.product = Products.objects.get(product_name="nutella")

	def test_detail_page_returns_200(self):
		"""
		Try to access page with valid query parameters
		It must return a http 200 code
		"""
		product_id = self.product.id_product
		response = self.client.get(reverse('purbeurre:detail', args=(product_id,)))
		self.assertEqual(response.status_code, 200)

	def test_detail_page_returns_404(self):
		"""
		Try to access page with invalid query parameters
		It must return a http 404 code
		"""
		product_id = self.product.id_product + 1
		response = self.client.get(reverse('purbeurre:detail', args=(product_id,)))
		self.assertEqual(response.status_code, 404)


# Search page tests
class SearchPageTestCase(TestCase):
	def setUp(self):
		"""
		Food data
		"""
		category = Categories.objects.create(category_name="Pâte à tartiner")
		Products.objects.create(
			id_product=1,
			product_name="nutella",
			category=category,
			nutriscore="c"
			)

		Products.objects.create(

			id_product=2,
			product_name="Nocciolata",
			category=category,
			nutriscore="a"
			)
		self.password = "1234abcd"
		self.user = User.objects.create_user(
			username="emanuele",
			password=self.password,
			email="email@email.com"
			)

		self.client = Client()
		self.origin = Products.objects.get(pk=1)
		self.replacement = Products.objects.get(pk=2)
		self.client.force_login(user=self.user)

	def test_search_page_returns_200(self):
		"""
		Try to access page with valid query parameters
		Request must return a http 200 code
		"""
		response = self.client.get(reverse('purbeurre:search'), {"query": "nutella"})
		self.assertEqual(response.status_code, 200)

	def test_search_page_returns_404(self):
		"""
		Try to access page with invalid query parameters
		Request must return a http 404 code
		"""
		response = self.client.get(reverse('purbeurre:search'), {"query": "kiri"})
		self.assertEqual(response.status_code, 404)

	def test_search_replace_product(self):
		"""
		Substitute food data
		"""
		url = reverse('purbeurre:search') + '?query=nutella'
		self.client.post(url, {
			"origin": self.origin.id_product,
			"replacement": self.replacement.id_product,
			})

		self.assertTrue(Substitutes.objects.exists())


# Register page
class RegisterTestPageCase(TestCase):
	"""
	User's registration page tests
	"""
	def setUp(self):
		"""
		Temporary data
		"""
		url = reverse('purbeurre:sign_up')
		data = {
			'username': 'john',
			'email': 'john@doe.com',
			'password1': 'abcdef123456',
			'password2': 'abcdef123456'
		}

		self.home_url=(reverse('purbeurre:account'))
		self.response = self.client.post(url, data)

    def test_register_page_returns_200(self):
    	"""
    	Simple call
    	It must return a http 200 code
    	"""
		response = self.client.get(reverse('purbeurre:sign_up'))
		self.assertEqual(response.status_code, 200)

	def test_registration(self):
		"""
		Try to register with valid data
		A user must have been created
		"""
		self.assertTrue(User.objects.exists())

	def test_csrf(self):
		"""
		Test for csfr token
		"""
		response = self.client.get(reverse('purbeurre:sign_up'))
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		"""
		Test for sign up form
		"""
		response = self.client.get(reverse('purbeurre:sign_up'))
		form = response.context.get('form')
		self.assertIsInstance(form, UserCreationForm)

	def test_user_authentication(self):
		"""
		Call for a new request to an arbitrary page.
		Request must have a 'user' on its context,
		after a successful sign up.
		"""
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

# Invalid registration page
class InvalidSignUpTests(TestCase):
	"""
	Invalid registration page tests
	"""
	def setUp(self):
		"""
		Simple call
		"""
		url = reverse('purbeurre:sign_up')
		self.response = self.client.post(url, {}) # submit an empty dictionary

	def test_signup_status_code(self):
		"""
        Try to access with invalid data
        Request must return a http 200 code (same registration form page)
		"""
		self.assertEquals(self.response.status_code, 200)

		def test_form_errors(self):
			"""
			Test error messages in registration form
			"""
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_dont_create_user(self):
		"""
		Try to access with invalid data
		Request must return an assert error message
		""" 
		self.assertFalse(User.objects.exists())


# Login page
class LoginTestPageCase(TestCase):
	"""
	User's login page tests
	"""
	def setUp(self):
		"""
		Temporary data
		"""
		self.username = "test"
		self.password = hash("1234abcd")
		self.user = User.objects.create_user(username=self.username, password=self.password)

	def test_login_page(self):
		"""
		Simple call
		It must return a http 200 code
		"""
		response = self.client.get(reverse('purbeurre:login'))
		self.assertEqual(response.status_code, 200)

	def test_login(self):
		"""
		Try to login with valid data
		Request must reurn a http 302 code to /login/
		"""
		response = self.client.post(reverse('purbeurre:login'), {
			"username": self.username,
			"password": self.password,
			})
		self.assertEqual(response.status_code, 302)

	def test_login_fail_username(self):
		"""
		Try to login with invalid username
		Request must return a http 200 code
		"""
		response = self.client.post(reverse('purbeurre:login'), {
			"username": ' ',
			"password": self.password,
			})
		self.assertEqual(response.status_code, 200)

	def test_login_fail_password(self):
		"""
		Try to login with invalid password
		"""
		response = self.client.post(reverse('purbeurre:login'), {
			"username": self.username,
			"password": 'defgzpzd,',
			})
		self.assertEqual(response.status_code, 200)

	def test_csrf(self):
		"""
		Test for csfr token
		"""
		response = self.client.get(reverse('purbeurre:login'))
		self.assertContains(response, 'csrfmiddlewaretoken')


# User account page
class AccountTestPageCase(TestCase):
	"""
	User account page tests
	"""
	def setUp(self):
		"""
		Temporary data
		"""
		url = reverse('purbeurre:account')
		self.data = {
			'username': 'john',
			'email': 'john@doe.com',
			'password': 'abcdef123456',
		}
		self.response = self.client.post(url, self.data)
		self.user = User.objects.create_user(**self.data)

	def test_account_page_returns_200(self):
		"""
		Try to access page while logged
		It must return a http 200 code
		"""
		self.client.login(**self.data)
		response = self.client.get(reverse('purbeurre:account'))
		self.assertEqual(response.status_code, 200)

	def test_account_page_redirects(self):
		"""
		Try to access page without being logged
		It must return a http 302 code to /account/
		"""
		response = self.client.get(reverse('purbeurre:account'))
		self.assertEqual(response.status_code, 302)


# Saved foods page
class SavedTestPageCase(TestCase):
	"""
	Saved foods page tests
	"""
	def setUp(self):
		"""
		Temporary data
		"""
		url = reverse('purbeurre:saved')
		self.data = {
			'username': 'john',
			'email': 'john@doe.com',
			'password': 'abcdef123456',
		}
		self.response = self.client.post(url, self.data)

		self.user = User.objects.create_user(**self.data)
		category = Categories.objects.create(category_name="Pâte à tartiner")

		origin = Products.objects.create(
			id_product=1,
			product_name="nutella",
			category=category
			)

		replacement = Products.objects.create(
			id_product=2,
			product_name="Nocciolata",
			category=category
			)

		Substitutes.objects.create(
			origin=origin,
			replacement=replacement,
			user=self.user)

		self.origin = Products.objects.get(pk=1)
		self.replacement = Products.objects.get(pk=2)

	def test_account_page_returns_200(self):
		"""
		Simple call
		It must return a http 200 code
		"""
		self.client.login(**self.data)
		response = self.client.get(reverse('purbeurre:saved'))
		self.assertEqual(response.status_code, 200)

	def test_account_page_redirects(self):
		"""
		Try to save a product being logged
		It must return a http 302 code to /saved/
		"""
		response = self.client.get(reverse('purbeurre:saved'))
		self.assertEqual(response.status_code, 302)

	def test_delete_substitute(self):
		"""
		Try to delete a food
		Substitutes list must be already created
		"""
		self.client.login(**self.data)
		self.client.post(reverse('purbeurre:saved'), {
			"origin": self.origin.id_product,
			"replacement": self.replacement.id_product,
			})
		self.assertFalse(Substitutes.objects.exists())