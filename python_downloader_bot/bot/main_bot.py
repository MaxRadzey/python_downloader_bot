from telebot.async_telebot import AsyncTeleBot
import telebot

from django.conf import settings


bot = AsyncTeleBot(settings.BOT_TOKEN)
telebot.logger.setLevel(settings.LOG_LEVEL)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)
