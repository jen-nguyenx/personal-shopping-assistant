import csv
from django.core.management.base import BaseCommand, CommandParser
from shoppingitems.models import Product

class Command(BaseCommand):
    help = "Bulk import product weight from a CSV file - used to calculate shipping fees"

    def add_arguments(self, parser: CommandParser) -> None:
        return parser.add_argument('csv_file_path', type=str)
    
    def handle(self, *args: csv.Any, **options: csv.Any) -> str | None:
        with open(options['csv_file_path'], 'r') as file:
            reader = csv.DictReader(file)
            products = []
            for row in reader:
                products.append(Product(
                    name=row['name'],
                    weight=row['weight']
                ))

            Product.objects.bulk_create(products)
            self.stdout.write(self.style.SUCCESS('Successfully imported products" weight'))