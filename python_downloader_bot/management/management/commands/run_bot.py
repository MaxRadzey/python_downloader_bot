import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from bot.main_bot import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запуск Бота'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Бот запущен!')
            asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL))
        except Exception as err:
            logger.error(f'Бот не запущен!\n{err}')
            # self.stdout.write(f'Бот не запущен!\n{err}')
