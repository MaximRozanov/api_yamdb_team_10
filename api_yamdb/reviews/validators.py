from datetime import datetime

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.',
        )


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            ('Введите корректный год'),
            params={'value': value},)
