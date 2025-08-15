import csv
import os
from django.core.management.base import BaseCommand
from tree_view.models import Chapter, Section
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'chapter_csv.csv')

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle foreign key assignment with error checking
                section = None
                id_parent_1_id = row.get('id_parent_1_id')
                try:        #the section will be the values willl save inside the id_parent_1_id
                    section = Section.objects.get(id=id_parent_1_id)     # id for the section , and the id_parent_1_id (FK) for chapter 
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Section with number {id_parent_1_id} does not exist. Skipping this chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid id for Section: {id_parent_1_id}. Skipping this chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle chapter creation
                try:
                    chapter, created = Chapter.objects.get_or_create(
                        id=row['id'],
                        defaults={
                            'label_en': row['label_en'],
                            'label': row['label'],
                            'id_parent_1': section,
                            'is_have_note':row['is_have_note'],
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added chapter: {chapter.label_en}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Chapter {chapter.label_en} already exists.'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error saving chapter {row["label_en"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing chapter {row["label_en"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Import completed.'))