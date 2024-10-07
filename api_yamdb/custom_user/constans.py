USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
MAX_LENGTH = 150

USERS_ROLE = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]
MAX_ROLE_LENGTH = max(len(role[0]) for role in USERS_ROLE)