from django.core.management.base import BaseCommand
from photosite.db import databaseClear, databaseInfo

# добавить обработку ключа --repair
class Command(BaseCommand):
    help = 'PhotoGallery database management'

    def handle(self, *args, **options):
        if options['clear']:
            databaseClear()
            print('PhotoGallery database cleared...')


        elif options['info']:
        	print('Photogallery database tables information:')	
        	info = databaseInfo()
        	for key in info:
        		print("     {}: {} rows".format(key,info[key]))

        else:
            print('Для информации используйте --help')

    def add_arguments(self, parser):
        parser.add_argument('-c','--clear',action='store_true', default=False, help='Очистка базы данных' )   
        parser.add_argument('-i','--info',action='store_true', default=False, help='Информация о базе данных' )       