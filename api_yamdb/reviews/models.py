from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import DISPLAYED_TEXT


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=50, null=True, default="user")
    bio = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название Категории"
    )
    slug = models.SlugField(
        unique=True
    )


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название Произведения"
    )
    year = models.PositiveSmallIntegerField(
        null=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='review'
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название Жанра"
    )
    slug = models.SlugField(
        unique=True
    )


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:DISPLAYED_TEXT]


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
