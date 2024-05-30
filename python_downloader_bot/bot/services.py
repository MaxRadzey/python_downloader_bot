import logging

from asgiref.sync import sync_to_async
from telebot.types import Chat, User, Message

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
        defaults=default_dict,
    )
    if create_status is False:
        logger.info(f'Пользователь обновлен {data.id} - @{username}')
    else:
        logger.info(f'Пользователь создан {data.id} - @{username}')
    return create_status


@sync_to_async
def get_language_code(message: Message) -> str:
    """Получает из БД язык пользователя.
    Args:
        message (Message): Объект сообщения
    Returns:
        str: Код языка
    """
    user = TelegramUser.objects.get(telegram_id=message.from_user.id)
    language_code = user.language
    return language_code


@sync_to_async
def set_language_code(message: Message, language_code: str) -> str:
    """Изменяет в БД язык пользователя.
    Args:
        message (Message): Объект сообщения
        language_code (str): Код языка
    Returns:
        str: Код языка
    """
    user = TelegramUser.objects.get(telegram_id=message.chat.id)
    user.language = language_code
    user.save()
    return user.language
