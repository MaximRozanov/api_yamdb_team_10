from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.',
        )
