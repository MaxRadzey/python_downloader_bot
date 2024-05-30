from django.db import models
from django.utils.translation import gettext as _


class TelegramUser(models.Model):
    """Users."""

    USER_ROLE = (
        ('admin', 'Админ'),
        ('free_status_user', 'Юзер с ограничениями'),
        ('paid_status_user', 'Юзер без ограничений')
    )
    USER_LANGUAGE = (
        ('eng', 'Английский'),
        ('rus', 'Русский')
    )

    telegram_id = models.PositiveBigIntegerField(
        _('telegrma ID'), db_index=True, unique=True
    )
    username = models.CharField(
        _('username'), max_length=150, blank=True, null=True
    )  # Добавить уникальность
    first_name = models.CharField(
        _('Имя'), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        _('Фамилия'), max_length=150, blank=True, null=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(
        verbose_name='Язык пользователя', max_length=5,
        blank=True, null=True,
        choices=USER_LANGUAGE, default='eng'
    )
    role = models.CharField(
        verbose_name='Статус юзера', max_length=40,
        choices=USER_ROLE, default='free_status_user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
