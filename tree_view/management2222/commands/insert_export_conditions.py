import csv
import os
from django.core.management.base import BaseCommand
from tree_view.models import HsCode, ExportFee
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'export_conditions.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get hs_code number and handle foreign key assignment
                hs_code = None #model Empty
                id_exportfee_id = row.get('id_exportfee_id') # Fk in the exportFee
                try:
                    hs_code = HsCode.objects.get(hs_code=id_exportfee_id) # id for ExportFee
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'hs_code with number {id_exportfee_id} does not exist. Skipping this sub chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Chapter: {id_exportfee_id}. Skipping this sub chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle sub-chapter creation
                try:
                    export_fee, created = ExportFee.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'export': row['export'],
                            'restriction_export': row['restriction_export'],
                            'export_en':row['export_en'],
                            'restriction_export_en': row['restriction_export_en'],
                            'id_exportfee':hs_code

                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {export_fee.export}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {export_fee.export} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["export"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["export"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))