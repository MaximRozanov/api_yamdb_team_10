from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from custom_user.constans import (
    MAX_LENGTH,
    USERS_ROLE,
    USER,
    ADMIN,
    MODERATOR,
    MAX_ROLE_LENGTH,
)
from custom_user.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username, RegexValidator(regex=r'^[\w.@+-]+\Z')),
        max_length=MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(max_length=254, unique=True, null=False)
    role = models.CharField(
        'роль',
        max_length=MAX_ROLE_LENGTH,
        choices=USERS_ROLE,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
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
