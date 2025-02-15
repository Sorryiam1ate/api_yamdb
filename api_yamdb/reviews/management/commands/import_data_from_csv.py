import csv

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models
from reviews.models import Genre, Review, Title


class Command(BaseCommand):
    """Универсальный метод для импорта csv файлов в базу"""
    help = 'Импортирует данные из CSV в указанную модель базы данных'

    def add_arguments(self, parser):
        parser.add_argument('app_label', type=str, help='Название приложения')
        parser.add_argument('model_name', type=str, help='Название модели')
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **kwargs):
        app_label = kwargs['app_label']
        model_name = kwargs['model_name']
        csv_file_path = kwargs['csv_file']

        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(
                f'Модель {model_name} не найдена.'))
            return

        self.import_csv(model, csv_file_path)

    def import_csv(self, model, csv_file_path):
        model_fields = {field.name: field for field in model._meta.fields}

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            objects_to_create = []

            for row in reader:
                filtered_data = {}

                for key, value in row.items():

                    field_name = key[:-3] if key.endswith(
                        "_id") and key[:-3] in model_fields else key

                    if field_name not in model_fields:
                        continue

                    field = model_fields[field_name]

                    if isinstance(field, models.ForeignKey):

                        related_model = field.related_model
                        try:
                            value = related_model.objects.get(id=int(value))

                            if (
                                issubclass(related_model, Title)
                                or issubclass(related_model, Review)
                                or issubclass(related_model, Genre)
                            ):
                                value = value.id

                        except related_model.DoesNotExist:
                            self.stderr.write(self.style.ERROR(
                                f'Объект {related_model.__name__} с ID {value} не найден'
                            ))
                            continue

                    filtered_data[key] = value

                objects_to_create.append(model(**filtered_data))

            model.objects.bulk_create(objects_to_create)
            self.stdout.write(self.style.SUCCESS('Импорт завершён!'))
