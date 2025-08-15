import csv
import os
from django.core.management.base import BaseCommand
from tariff.models import HsCode, Sub_Chapter
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'item_csv.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get Chapter number and handle foreign key assignment
                sub_chapter = None
                id_parent_3_id = row.get('id_parent_3_id')
                try:
                    sub_chapter = Sub_Chapter.objects.get(id=id_parent_3_id)
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Chapter with number {id_parent_3_id} does not exist. Skipping this sub chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Chapter: {id_parent_3_id}. Skipping this sub chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle sub-chapter creation
                try:
                    hs_code, created = HsCode.objects.get_or_create(
                        hs_code=row['id'],
                        defaults={
                            'label_en': row['label_en'],
                            'label': row['label'],
                            'review_en':row['review_en'],
                            'review':row['review'],
                            'review_value':row['review_value'],
                            'id_parent_3': sub_chapter,

                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added sub chapter: {sub_chapter.label_en}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sub chapter {sub_chapter.label_en} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving sub chapter {row["label_en"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing sub chapter {row["label_en"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))