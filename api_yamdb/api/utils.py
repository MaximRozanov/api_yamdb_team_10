from random import choices


def generate_confirmation_code(length=4):
    return ''.join(choices('0123456789', k=length))
