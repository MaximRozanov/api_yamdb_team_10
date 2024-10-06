from random import choices


def generate_confirmation_code():
    return ''.join(choices('123456789', k=4))