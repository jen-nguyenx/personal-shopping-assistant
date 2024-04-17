import csv
import os
from django.core.management.base import BaseCommand, CommandParser
from shoppingitems.models import Product
import invoice_processor.settings as settings

class Command(BaseCommand):
    help = "Bulk import product weight from a CSV file - used to calculate shipping fees"

    def add_arguments(self, parser: CommandParser) -> None:
        return parser.add_argument('csv_file_path', type=str)
    
    def handle(self, *args, **options) -> str | None:
        file_path = os.path.join(settings.DATA_DIR, 'yourfile.csv')
        print(settings.DATA_DIR)  # Add this in your views or commands to check the path

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            products = []
            for row in reader:
                products.append(Product(
                    name=row['name'],
                    weight=row['weight']
                ))

            Product.objects.bulk_create(products)
            self.stdout.write(self.style.SUCCESS('Successfully imported products" weight'))