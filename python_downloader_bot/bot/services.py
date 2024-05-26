import logging

from asgiref.sync import sync_to_async
from telebot.types import Chat, User

from bot.models import TelegramUser

logger = logging.getLogger(__name__)


@sync_to_async
def update_or_create_user(data: Chat | User) -> bool:
    try:
        data = getattr(data, 'chat')
    except AttributeError:
        data = data
    first_name = data.first_name
    if not data.first_name:
        first_name = ''
    last_name = data.last_name
    if not data.last_name:
        last_name = ''
    username = data.username
    if not data.username:
        username = ''
    default_dict = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username
    }
    telegram_user, create_status = TelegramUser.objects.get_or_create(
        telegram_id=data.id,
        # username=username,
        # first_name=first_name,
        # last_name=last_name,
        defaults=default_dict,
    )
    if create_status is False:
        logger.info(f'Пользователь обновлен {data.id} - @{username}')
    else:
        logger.info(f'Пользователь создан {data.id} - @{username}')
    return create_status
