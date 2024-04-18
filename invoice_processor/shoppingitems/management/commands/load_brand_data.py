from typing import Any
from django.core.management.base import BaseCommand
from shoppingitems.models import Brand
from services.web_scraper import get_brand_names
from services.static_url import URL_LIST

class Command(BaseCommand):
    help = 'Load brand data from specified URLs into the database'

    def handle(self, *args: Any, **options: Any) -> str | None:
        brand_df = get_brand_names(URL_LIST)
        for index, row in brand_df.iterrows():
            try:
                Brand.objects.get_or_create(
                    name=row['name'],
                    category=row['category']
                )

                self.stdout.write(self.style.SUCCESS(f'Processed entry: {row["name"]} - {row["category"]}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to process entry {row["name"]} - {row["category"]} due to {str(e)}'))
