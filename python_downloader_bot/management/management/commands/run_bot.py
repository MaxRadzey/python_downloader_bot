import asyncio
from django.core.management.base import BaseCommand

from bot.main_bot import bot


class Command(BaseCommand):
    help = 'Запуск Бота'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Бот запущен!')
            asyncio.run(bot.polling())
        except Exception:
            self.stdout.write('Бот не запущен!')
