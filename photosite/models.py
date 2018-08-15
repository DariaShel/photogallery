from django.db import models

# Create your models here.
class Years(models.Model):
	title = models.PositiveSmallIntegerField()
class Directories(models.Model):
	title = models.CharField(max_length=150)