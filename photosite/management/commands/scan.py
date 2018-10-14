from django.core.management.base import BaseCommand
from photosite.scan import ScanAll

class Command(BaseCommand):
    help = 'Сканирование соллекции фотографий'

    def handle(self, *args, **options):
        print('Scan of photo')
        ScanAll(options['verbosity'])

    def add_arguments(self, parser):
    	pass
        #parser.add_argument('-v','--verbose',action='store_true', default=False, help='Подробный вывод информации о сканировании' )            