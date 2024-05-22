import logging

from telebot.async_telebot import AsyncTeleBot
import telebot

from django.conf import settings


bot = AsyncTeleBot(settings.BOT_TOKEN)
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


# @bot.chat_member_handler()
# async def chat_member_handler_bot(message):
#     # logger.info(f'aaaa - {message}')


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    text = message.text
    # logger.info(f'aaaa - {message}')
    logger.info(f'{user_id=}')
    logger.info(f'{full_name=}')
    logger.info(f'{username=}')
    logger.info(f'{text=}')
    # print(11)
    await bot.reply_to(message, message.text)
