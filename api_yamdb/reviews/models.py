from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import validate_year
from users.models import User

from .constants import DISPLAYED_TEXT, MAX_SCORE, MIN_SCORE, NAME_MAX_LENGTH


class CategoryGenre(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenre):
    class Meta(CategoryGenre.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenre):
    class Meta(CategoryGenre.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.SmallIntegerField(
        verbose_name='Год издания',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория'
    )
    description = models.TextField(
        'Описание',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='Genre_title',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:DISPLAYED_TEXT]

    def get_genre_list(self):
        return ', '.join([str(genre) for genre in self.genre.all()])


class ReviewComment(models.Model):
    text = models.TextField('Текст отзыва')
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
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews_written'
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments_written'
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанр_Произведение'
        verbose_name_plural = 'Жанры_Произведения'

    def __str__(self):
        return self.genre
