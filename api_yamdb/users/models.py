from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from reviews.constants import (
    EMAIL_MAX_LENGTH,
    PATTERN_USERNAME,
    USERNAME_MAX_LENGTH
)

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(
        'Имя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            validate_username,
            RegexValidator(regex=PATTERN_USERNAME),
        )
    )

    email = models.EmailField(
        'Email',
        max_length=EMAIL_MAX_LENGTH,
        blank=True
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Роль',
        max_length=len(max([x for x, _ in CHOISES], key=len)),
        choices=CHOISES, default=USER
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('role',)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return bool(self.role == User.ADMIN or self.is_superuser)
