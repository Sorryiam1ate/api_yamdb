from rest_framework.exceptions import ValidationError
from reviews.constants import RESTRICTED_NAME


def validate_username(value):
    if value in RESTRICTED_NAME:
        raise ValidationError('Недопустимое имя пользователя!')
