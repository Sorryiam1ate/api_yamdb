from rest_framework.exceptions import ValidationError

from .models import User


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегестрирован')
