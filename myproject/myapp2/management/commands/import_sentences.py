import pandas as pd
from django.core.management.base import BaseCommand
from myapp2.models import Sentences

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            Sentences.objects.create(
                sentence=row['sentence'],
                nmb_sent=row['nmb_sent'],
                author=row['author'],
                title=row['title'], 
                nmb_text=row['nmb_text']           
            )