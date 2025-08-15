import csv
import os
from django.core.management.base import BaseCommand
from tariff.models import Notes_section, Section
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Import notes_section from CSV file into the database'

    def handle(self, *args, **kwargs):
        # Path to CSV file relative to this script
        csv_file_path = os.path.join(os.path.dirname(__file__), 'section_notes_csv.csv')

        try:
            with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                self.stdout.write(f"Detected fields: {reader.fieldnames}")  # Debug header info

                for row in reader:
                    try:
                        id_section_value = row.get('id_section_id')
                        id_section_id = None

                        if id_section_value:
                            try:
                                id_section_id = Section.objects.get(id=id_section_value)
                            except Section.DoesNotExist:
                                self.stdout.write(self.style.ERROR(f"Section with ID {id_section_value} not found."))

                        note_id = row.get('id')
                        if not note_id:
                            self.stdout.write(self.style.ERROR("Missing 'id' field in row, skipping."))
                            continue

                        note, created = Notes_section.objects.get_or_create(
                            id=note_id,
                            defaults={
                                'id_section': id_section_id,
                                'note_a': row.get('note_a') or None,
                                'note_b': row.get('note_b') or None,
                                'note_c': row.get('note_c') or None,
                                'note_num': row.get('note_num') or None,
                                'note_a_en': row.get('note_a_en') or None,
                                'note_b_en': row.get('note_b_en') or None,
                                'note_c_en': row.get('note_c_en') or None,
                                'note_num_en': row.get('note_num_en') or None,
                            }
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f'✅ Added note {note_id}'))
                        else:
                            self.stdout.write(self.style.WARNING(f'⚠️ Note {note_id} already exists'))

                    except ValidationError as ve:
                        self.stdout.write(self.style.ERROR(f"Validation error: {ve}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Unhandled error in row {row}: {e}"))

            self.stdout.write(self.style.SUCCESS('🎉 Notes import completed successfully.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ CSV file not found: {csv_file_path}"))
