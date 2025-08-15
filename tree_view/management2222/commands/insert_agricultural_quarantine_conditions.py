import csv
import os
from django.core.management.base import BaseCommand
from tree_view.models import HsCode, Stone_Farming
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'agricultural_quarantine_csv.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get hs_code number and handle foreign key assignment
                hs_code = None #model Empty
                id_stone_id = row.get('id_stone_id') # Fk in the exportFee
                try:
                    hs_code = HsCode.objects.get(hs_code=id_stone_id) # id for ExportFee
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'hs_code with number {id_stone_id} does not exist. Skipping this sub chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Chapter: {id_stone_id}. Skipping this sub chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle sub-chapter creation
                try:
                    stone_farming, created = Stone_Farming.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'ston_import': row['ston_import'],
                            'ston_import_en': row['ston_import_en'],
                            'ston_import_notes': row['ston_import_notes'],
                            'ston_import_notes_en': row['ston_import_notes_en'],
                            'ston_export':row['ston_export'],
                            'ston_export_en':row['ston_export_en'],
                            'ston_export_notes': row['ston_export_notes'],
                            'ston_export_notes_en': row['ston_export_notes_en'],
                            'id_stone':hs_code

                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {stone_farming.ston_import}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {stone_farming.ston_import} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["ston_import"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["ston_import"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))