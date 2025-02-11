from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import DISPLAYED_TEXT
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название Категории'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название Жанра'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название Произведения'
    )
    year = models.PositiveSmallIntegerField(
        null=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles'
    )
    description = models.TextField(
        'Описание',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='Genre_title',
    )

    class Meta:
        ordering = ('name',)


class ReviewComment(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:DISPLAYED_TEXT]


class Review(ReviewComment):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )

    class Meta(ReviewComment.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
