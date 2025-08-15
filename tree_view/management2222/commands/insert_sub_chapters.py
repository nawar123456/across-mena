import csv
import os
from django.core.management.base import BaseCommand
from tree_view.models import Sub_Chapter, Chapter
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import sub chapters from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'sub_chapter_csv.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get Chapter number and handle foreign key assignment
                chapter = None # chapter 
                id_parent_2_id = row.get('id_parent_2_id') # id_parent_2_id the colu in the Sub
                try:
                    chapter = Chapter.objects.get(id=id_parent_2_id)#for connect the FK id to Chapter
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Chapter with number {id_parent_2_id} does not exist. Skipping this sub chapter.'))
                    continue  # Skip this iteration
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid number for Chapter: {id_parent_2_id}. Skipping this sub chapter.'))
                    continue  # Skip this iteration

                # Use get_or_create to handle sub-chapter creation
                try:
                    sub_chapter, created = Sub_Chapter.objects.get_or_create(  #like what we said we will create the Sub_Chapter Table 
                        id=row['id'],
                        defaults={
                            'label_en': row['label_en'],
                            'label': row['label'],
                            'review_en':row['review_en'],
                            'id_parent_2': chapter,

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