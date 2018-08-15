from django.contrib import admin
from photosite.models import Years
# Register your models here.
class Years_admin(admin.ModelAdmin):
	list_display = ('title',)

admin.site.register(Years, Years_admin)