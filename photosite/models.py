from django.db import models

# Create your models here.
class Favorites(models.Model):
	user = models.CharField(max_length=150)
	photo = models.TextField()