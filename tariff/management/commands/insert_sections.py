import csv
import os
from django.core.management.base import BaseCommand
from tariff.models import Section 
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
     help = 'Import sections from a CSV file into the database'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
     def handle(self, *args, **kwargs):
        # Construct the path to the CSV file relative to the current file
        csv_file_path = os.path.join(os.path.dirname(__file__), 'section_csv.csv')

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Use get_or_create to avoid duplicates
                    section, created = Section.objects.get_or_create(
                        number=row['id'],
                        id=row['id'],

                        defaults={
                            'name_en': row['name_en'],
                            'name': row['name'],
                            'label_en': row['label_en'],
                            'label': row['label'],
                            'start': row['start'],
                            'end': row['end'],
                            'number': row['number'],
                            'is_have_note': row['is_have_note'],
                            # 'image': row['image']  # Uncomment and use if necessary
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added section: {section.name_en}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Section {section.name_en} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving section {row["name_en"]}: {e}'))
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Missing field in row {row}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing section {row.get("name_en", "Unknown")}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))