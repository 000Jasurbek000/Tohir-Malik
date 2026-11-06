import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from dictionary_app.models import DictionaryEntry


class Command(BaseCommand):
    help = 'Load all dictionary CSV files into SQLite.'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[3]
        csv_files = {
            'green': base_dir / 'green.csv',
            'yellow': base_dir / 'yellow.csv',
            'red': base_dir / 'red.csv',
            'purple': base_dir / 'purple.csv',
        }

        created = 0
        updated = 0

        for category_key, file_path in csv_files.items():
            if not file_path.exists():
                self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path.name}'))
                continue

            with file_path.open('r', encoding='utf-8-sig', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row:
                        continue

                    title = (row.get('Frazeologik birlik') or '').strip()
                    if not title or title.isdigit():
                        continue

                    meaning = (row.get('Ma’nosi') or '').strip()
                    notes = (row.get("Lingvoma’naviy xususiyati") or '').strip()
                    pages = (row.get('Bet(lar)') or '').strip()
                    example = (row.get('Frazeologik birlik qatnashgan gap') or '').strip()

                    obj, is_created = DictionaryEntry.objects.get_or_create(
                        title=title,
                        category=category_key,
                        defaults={
                            'meaning': meaning,
                            'notes': notes,
                            'example': example,
                            'pages': pages,
                            'source_file': file_path.name,
                            'raw_row': str(row),
                        },
                    )

                    if not is_created:
                        obj.meaning = meaning
                        obj.notes = notes
                        obj.example = example
                        obj.pages = pages
                        obj.source_file = file_path.name
                        obj.raw_row = str(row)
                        obj.save()
                        updated += 1
                    else:
                        created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Loaded dictionary CSV data: {created} created, {updated} updated.'
        ))
