from django.apps import apps
from django.core.management.base import BaseCommand
import csv


class Command(BaseCommand):
    """Универсальный метод для импорта csv файлов в базу"""
    help = 'Импортирует данные из CSV в указанную модель базы данных'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Название модели')
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        csv_file_path = kwargs['csv_file']

        try:
            model = apps.get_model('reviews', model_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(
                f'Модель {model_name} не найдена.'))
            return

        self.import_csv(model, csv_file_path)

    def import_csv(self, model, csv_file_path):
        model_fields = [field.name for field in model._meta.fields]
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            objects_to_create = []
            for row in reader:
                filtered_data = {key: value for key,
                                 value in row.items() if key in model_fields}
                objects_to_create.append(model(**filtered_data))

            model.objects.bulk_create(objects_to_create)
            self.stdout.write(self.style.SUCCESS('Импорт в завершён!'))
