from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.constants import EMAIL_LENGTH, ROLE_LENGTH


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )

    email = models.EmailField(
        'Email', max_length=EMAIL_LENGTH, unique=True
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField('Роль', max_length=ROLE_LENGTH,
                            choices=CHOISES, default='user')

    class Meta:

        ordering = ('role',)

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER
