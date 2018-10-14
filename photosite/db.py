import os
from photosite.models import  Favorites, Photo

def databaseClear():
	Favorites.objects.all().delete()
	Photo.objects.all().delete()

def databaseInfo():
    info = {}
    info['Favorites'] = Favorites.objects.count()
    info['Photo'] = Photo.objects.count()
    return info

def databaseRepair()
    # Проверка присутсвия Thumbnail и Preview для всех строк из БД - если что-то отсуствует - создать
    # Проверка наличия основного фото для всех строк из БД - если основное фото уалено удалить Thumbnail и Preview и строку из БД
	pass

def addImage(relPath, title):
	# пытемся найти в БД строку с relPath - если она есть то ничего не делаем
	# Создание Thumbnail и Preview в соответсвующих каталогах, Если это еще не сдалано
	print(relPath)
	im = Photo.objects.get_or_create(relpath=relPath, title=title)
	return im
