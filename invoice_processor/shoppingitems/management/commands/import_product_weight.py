import csv
import os
from django.core.management.base import BaseCommand, CommandParser
from shoppingitems.models import Product
import invoice_processor.settings as settings
from services.rtf_converter import convert_rtf_to_csv
from datetime import datetime

class Command(BaseCommand):
    help = "Bulk import product weight from a CSV file - used to calculate shipping fees"

    def add_arguments(self, parser: CommandParser) -> None:
        return parser.add_argument('csv_file_path', type=str)
    
    def handle(self, *args, **options) -> str | None:
        csv_file_path = options['csv_file_path']
        time = datetime.now()

        # Convert rtf data to csv
        file_path = os.path.join(settings.DATA_DIR, csv_file_path)
        convert_rtf_to_csv(file_path, f'product_weight_{time}.csv')

        csv_path = os.path.join(settings.DATA_DIR, f'product_weight_{time}.csv')

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                Product.objects.update_or_create(
                    name=row['name'],
                    weight=row['weight']
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported products' weight"))