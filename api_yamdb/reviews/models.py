import random

from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.contrib.auth.models import AbstractUser

from .validators import validate_username, year_validator
from .constants import (USER,
                        ADMIN,
                        MODERATOR,
                        MAX_LENGTH,
                        USERS_ROLE,
                        NAME_MAX_LENGTH,
                        SLUG_MAX_LENGTH)


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    year = models.IntegerField(validators=[year_validator, ])
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username, RegexValidator(regex=r'^[\w.@+-]+\Z')),
        max_length=MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(max_length=254, unique=True, null=False)
    role = models.CharField(
        max_length=20, choices=USERS_ROLE, default=USER, blank=True
    )
    bio = models.TextField(
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
