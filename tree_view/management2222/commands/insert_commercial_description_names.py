import csv
import os
import re 
from django.core.management.base import BaseCommand
from tree_view.models import HsCode,Commercial_Description
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'commercial_description_names_csv.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get Item number
                hs_code = None
                id_desc_id = row.get('id_desc_id')
                try:
                    hs_code = HsCode.objects.get(hs_code=id_desc_id)
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Item with number {item_number} does not exist. Skipping this commercial description name.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.ERROR(f'Invalid number for Item: {item_number}. Skipping this commercial description name.'))
                    continue  # Skip this iteration
                try:
                    com_desc, created = Commercial_Description.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'second_description': row['second_description'],
                            'id_desc':hs_code

                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {com_desc.second_description}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {com_desc.second_description} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["second_description"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["second_description"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))