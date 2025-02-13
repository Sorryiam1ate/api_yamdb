from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(f'Год не может быть больше {current_year}!')
