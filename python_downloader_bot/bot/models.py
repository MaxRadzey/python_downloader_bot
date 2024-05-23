from django.db import models
from django.utils.translation import gettext as _


class TelegramUser(models.Model):
    """Users."""

    telegram_id = models.PositiveBigIntegerField(
        _('telegrma ID'), db_index=True, unique=True
    )
    username = models.CharField(
        _('username'), max_length=150, blank=True, null=True
    )
    first_name = models.CharField(
        _('Имя'), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        _('Фамилия'), max_length=150, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
