from django.db import models

from django.contrib.auth.models import User
from  django.db.models import CASCADE

# Create your models here.
class Favorites(models.Model):
	uid = models.ForeignKey(User, on_delete=CASCADE, default=None)
	path = models.CharField(max_length=512)
	title = models.CharField(max_length=32, default=None, null=True)