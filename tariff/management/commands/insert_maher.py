import csv
import os
from django.core.management.base import BaseCommand
from tariff.models import HsCode, Sub_Chapter
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class Command(BaseCommand):
    help = 'Import HsCode data from formatted.csv into the database'

    def handle(self, *args, **kwargs):
        # 🗂️ CSV path - same dir as the command file
        csv_file_path = os.path.join(os.path.dirname(__file__), 't10.csv')
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                sub_chapter = None

                # ✅ Find parent Sub_Chapter
      

                try:
                    # ✅ Create or update HsCode
                    hs_code, created = HsCode.objects.update_or_create(
                        hs_code=row['band'],  # 👈 from CSV
                        defaults={
                            'label': row.get('name'),
                            'import_fee': row.get('priceImport') or 0,
                            'ser_all': row.get('clearanceFee') or 0,
                            'review_en': row.get('material'),
                            'export_fee': row.get('clearanceFeeExport') or 0,
                            'exp_ser_Fe': row.get('priceExport') or 0,
                            'type': row.get('type') or 0,
                            'full_import_fee': row.get('priceFull') or 0,



                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'✅ Created HSCode: {hs_code.hs_code}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'♻️ Updated HSCode: {hs_code.hs_code}'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'❌ Validation error: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'💥 Unexpected error: {e}'))

        self.stdout.write(self.style.SUCCESS('🎉 HSCode import completed successfully.'))
