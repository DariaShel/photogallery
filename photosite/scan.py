import os

from django.conf import settings

from photosite.models import  Favorites, Photo
from photosite.db import addImage

def ScanAll(verbosity=0):
	for full_path, dirs, files in os.walk(settings.ROOT_PATH):
		for name in files:
			(n,e)=os.path.splitext(name)
			if e.lower() in settings.VALID_EXT:
				rel_path=os.path.relpath(full_path,settings.ROOT_PATH)
				if verbosity>1:
					print('Adding file {} in relative path: {}'.format(name, rel_path))
				img=addImage(os.path.join(rel_path,name), name)	
