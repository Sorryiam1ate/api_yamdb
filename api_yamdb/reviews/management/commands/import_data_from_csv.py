import csv
from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'Импортирует данные из CSV в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

                self.stdout.write(self.style.SUCCESS(
                    f'Запись "{row["name"]}" успешно добавлена!'))

        self.stdout.write(self.style.SUCCESS(
            'Все данные успешно импортированы!'))
