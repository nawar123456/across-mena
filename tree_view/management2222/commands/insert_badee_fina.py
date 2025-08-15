import csv
import os
from django.core.management.base import BaseCommand
from tariff.models import Finance, SyrianItem
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import Financing for items from a CSV file into the database'
 
    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'finance_csv.csv')

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle foreign key assignment with error checking
                item = None
                item_number = row.get('id_finance_id')
                try:
                    item = SyrianItem.objects.get(number=item_number)

                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Item with number {item_number} does not exist. Skipping this Item.'))
                    continue  # Skip this iteration

                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Item: {item_number}. Skipping this Item.'))
                    continue  # Skip this iteration
                
                # Get the days number:
                try:
                    number_of_days_str = row['finance_en'].split()[0]
                    number_of_days = self.text_to_number.get(number_of_days_str, None)

                    if number_of_days is None:
                        self.stdout.write(self.style.WARNING(f'Invalid number of days: {number_of_days_str}. Skipping this row.'))
                        continue  # Skip

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Invalid number of days due to error: {e}.'))
                    continue  # Skip

                # Use get_or_create to handle chapter creation
                try:
                    finance, created = Finance.objects.get_or_create(
                        duration=number_of_days,
                        item=item
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added finance for item: {finance.item.number}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'finance for item {finance.item.number} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving finance for item {row["id_finance_id"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing saving finance for item {row["id_finance_id"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))