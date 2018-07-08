from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
	category_name = models.CharField(max_length=255, unique=True)
	def __str__(self):
		return self.category_name


class Dishes(models.Model):
	dish_id = models.BigIntegerField(primary_key=True)
	dish_name = models.CharField(max_length=255)
	url = models.URLField()
	img = models.URLField()
	fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	saturated_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	salt = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	sugar = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	nutriscore = models.CharField(max_length=1, null=True)
	category = models.ForeignKey("Categories", on_delete=models.CASCADE)

	def __str__(self):
		return str({
			"dish_id": self.dish_id,
			"dish_name": self.dish_name,
			"url": self.url,
			"image": self.img,
			"nutriscore": self.nutriscore,
			"category": self.category
			})


class Substitutes(models.Model):
	origin_dish = models.ForeignKey(Dishes, related_name='origin_dish', on_delete=models.CASCADE)
	alternative_dish = models.ForeignKey(Dishes, related_name='alternative_dish', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str({
			"origin_dish": self.origin_dish,
			"alternative_dish": self.alternative_dish,
			"user": self.user
			})
