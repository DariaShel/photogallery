from django.contrib import admin
from photosite.models import Favorites
# Register your models here.
class Favorites_Admin(admin.ModelAdmin):
	list_display =('uid','path','title')

admin.site.register(Favorites, Favorites_Admin)