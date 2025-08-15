import csv
import os
from django.core.management.base import BaseCommand
from tree_view.models import Finance, HsCode
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import Financing for items from a CSV file into the database'
 
    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'finance_csv.csv')

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle foreign key assignment with error checking
                hs_code = None
                id_finance_id = row.get('id_finance_id')
                try:
                    hs_code = HsCode.objects.get(hs_code=id_finance_id)

                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Item with number {id_finance_id} does not exist. Skipping this Item.'))
                    continue  # Skip this iteration

                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Item: {id_finance_id}. Skipping this Item.'))
                    continue  # Skip this iteration
                
               

                # Use get_or_create to handle chapter creation
                try:
                    financee, created = Finance.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'finance': row['finance'],
                            'finance_en':row['finance_en'],
                            'id_finance':hs_code


                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {financee.finance}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {financee.finance} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["finance"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["finance"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))