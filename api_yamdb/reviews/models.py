from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="review"
    )
    text = models.TextField(
        verbose_name="Текст ревью"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(
        verbose_name="Текст комментария"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    pub_date = models.DateTimeField(
        'Дата публикации'
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
