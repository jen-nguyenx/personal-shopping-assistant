from typing import Any
import pandas as pd
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandParser
from shoppingitems.models import Product, Brand, Transaction
import invoice_processor.settings as settings
import requests
import re
import os
from constants import SHIPPING_COST_AUD

class Command(BaseCommand):
    help = 'Process tax invoice'

    def add_arguments(self, parser: CommandParser) -> None:
        # Specify file name for processed invoice
        date = datetime.now().date()
        parser.add_argument(
            '--filename',
            type = str,
            help = 'Name of the output file'
        )

        # Specify the start date to which the invoice gets processed
        parser.add_argument(
            '--start-date',
            type = lambda s: datetime.strptime(s, '%d%m%y').date(),
            required = True,
            help = 'Start date in DDMMYY format to filter invoice files'
        )

        # Specify the end date to which the invoice gets processed
        parser.add_argument(
            '--end-date',
            type = lambda s: datetime.strptime(s, '%d%m%y').date(),
            default = date,
            help = 'End date in DDMMYY format to filter invoice files'
        )
    
    
    def handle(self, *args: Any, **options: Any) -> None:
        # Get arguments from parser
        start_date = options['start_date']
        end_date = options['end_date']
        filename = options.get('filename', f'supplements_price_{datetime.now().date()}')

        # Load data
        self.stdout.write(self.style.SUCCESS(f'Processing invoices from {start_date} to {end_date}'))
        invoice_df = self.get_invoices(start_date, end_date)

        # Process data
        self.process_invoices(invoice_df)
    

    def get_invoices(self, start_date, end_date, prefix: str = 'invoice'):
        file_pattern = '{}_{}.csv'
        files = []

        delta_date = end_date - start_date
        date_list = [start_date + timedelta(days=x) for x in range(delta_date.days + 1)]

        for date in date_list:
            # Convert the date into desired file name pattern
            file_name = file_pattern.format(prefix, date.strftime('%d%m%y'))
            file_path = os.path.join(settings.DATA_DIR, file_name)

            # Skip files that do not exist
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'No invoices found for {date}'))
                continue
            else:
                self.stdout.write(self.style.SUCCESS(f'Processing file {file_name}'))            
                files.extend(file_path)
        
        invoice_df = pd.concat([pd.read_csv(file) for file in files])

        return invoice_df
    

    def process_invoices(self, invoice_df: pd.DataFrame):
        invoice_df['Brand'] = invoice_df['Product'].apply(self.extract_brand_info)
        invoice_df['Weight'] = invoice_df['Weight'].apply(lambda x: self.get_product_weight(x))
        

        return None



    def extract_brand_info(self, product_name: pd.Series):
        brand_list = Brand.objects.all().values_list('name', flat=True)
        brand_pattern = '|'.join([re.escape(brand) for brand in brand_list])

        match = re.search(brand_pattern, product_name, re.IGNORECASE)
        if match:
            # Return the first matching brand names
            return match.group(0)  
        return "Unknown" 
    

    def get_product_weight(self, product_name: pd.Series):
        product_detail = Product.objects.filter(name__icontains=product_name)
        if product_detail.exists():
            weight = product_detail.first().weight
            return float(weight)
        self.stdout.write(self.style.WARNING(f'No weight recorded for {product_name}'))
        return 0