from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from .validators import year_validator
from .constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from custom_user.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг', unique=True, max_length=SLUG_MAX_LENGTH
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг', unique=True, max_length=SLUG_MAX_LENGTH
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=NAME_MAX_LENGTH
    )
    year = models.IntegerField(
        verbose_name='Год выхода',
        validators=[
            year_validator,
        ],
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', through='GenreTitle'
    )
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, verbose_name='Произведение', on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre, verbose_name='Жанр', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Статья',
    )
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, message='Оценка не может быть больше 10'),
            MinValueValidator(1, message='Оценка не может быть ниже 1'),
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    def __str__(self):
        return f'{self.title} автора {self.author}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    def __str__(self):
        return f'{self.author} ккомментирует {self.review}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
