import csv
import os
from django.core.management.base import BaseCommand
from tree_view.models import HsCode, Notes_fee
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'items_notes_csv.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get hs_code number and handle foreign key assignment
                hs_code = None #model Empty
                id_fee_id = row.get('id_fee_id') # Fk in the exportFee
                try:
                    hs_code = HsCode.objects.get(hs_code=id_fee_id) # id for ExportFee
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'hs_code with number {id_fee_id} does not exist. Skipping this sub chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Chapter: {id_fee_id}. Skipping this sub chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle sub-chapter creation
                try:
                    hs_code_notes, created = Notes_fee.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'note_a': row['note_a'],
                            'note_b':row['note_b'],
                            'additional_note':row['additional_note'],
                            'name_addition': row['name_addition'],
                            'additional_note_en':row['additional_note_en'],
                            'name_a_en': row['name_a_en'],
                            'name_b_en':row['name_b_en'],
                            'note_b_en': row['note_b_en'],
                            'note_a_en':row['note_a_en'],
                            'name_a': row['name_a'],
                            'name_b':row['name_b'],
                            'name_addition_en':row['name_addition_en'],
                            'id_fee':hs_code


                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {hs_code_notes.name_a}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {hs_code_notes.name_a} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["name_a"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["name_a"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))