from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import DISPLAYED_TEXT, NAME_LENGTH, SLUG_LENGTH
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название Категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_LENGTH,
        verbose_name='Слаг Категории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название Жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_LENGTH,
        verbose_name='Слаг Жанра'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название Произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год издания'
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
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


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
        'Оценка',
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
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Жанр_Произведение'
        verbose_name_plural = 'Жанры_Произведения'
