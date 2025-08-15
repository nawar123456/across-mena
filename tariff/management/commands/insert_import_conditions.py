import csv
import os
from django.core.management.base import BaseCommand
from tariff.models import HsCode, ImportFee
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'import_conditions_no_rest.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get hs_code number and handle foreign key assignment
                hs_code = None #model Empty
                id_importfee_id = row.get('id_importfee_id') # Fk in the exportFee
                try:
                    hs_code = HsCode.objects.get(hs_code=id_importfee_id) # id for ExportFee
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'hs_code with number {id_importfee_id} does not exist. Skipping this sub chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Chapter: {id_importfee_id}. Skipping this sub chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle sub-chapter creation
                try:
                    import_fee, created = ImportFee.objects.get_or_create(
                        id=row['id'],
                        defaults={
                           
                            'id_importfee':hs_code


                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {import_fee.document_import_en}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {import_fee.document_import_en} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["document_import_en"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["document_import_en"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))