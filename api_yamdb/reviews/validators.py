from datetime import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            ('Введите корректный год'),
            params={'value': value},)
