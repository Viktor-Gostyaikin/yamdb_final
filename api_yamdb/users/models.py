from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.crypto import get_random_string


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField(
        'email address', max_length=254, blank=False, unique=True)
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES,
        max_length=9, default=USER,
        error_messages={'validators': 'Выбрана несуществующая роль'}
    )
    confirmation_code = models.CharField(
        'confirmation_code', blank=True, max_length=128)
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def set_confirmation_code(self, confirmation_code):
        self.confirmation_code = make_password(confirmation_code)

    def make_confirmation_code(
        self, length=6,
        allowed_chars='abcdefghjkmnpqrstuvwxyz'
            'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    ):
        '''
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have 'I' or
        'O' or letters and digits that look similar -- just to avoid confusion.
        '''

        return get_random_string(length, allowed_chars)

    def check_confirmation_code(self, raw_confirmation_code: str) -> bool:
        return check_password(raw_confirmation_code, self.confirmation_code)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
