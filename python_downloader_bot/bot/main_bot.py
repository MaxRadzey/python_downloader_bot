import logging
import requests
from bs4 import BeautifulSoup
import ffmpeg

from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot import types
from telebot.types import Message
import moviepy.editor as mpy

from django.conf import settings
from bot.middleware import CustomMiddleware, AntifloodMiddleware
from bot.language_dict import messages
from bot.services import get_language_code, set_language_code


# url = 'https://www.tiktok.com/@_il9_/video/7043465037918326018'
# TikTok URL https://www.tiktok.com/@_il9_/video/7043465037918326018


def get_video(url):

    cookies = {
        '_ga': 'GA1.1.1724469622.1716577356',
        '_ga_ZSF3D6YSLC': 'GS1.1.1716577356.1.1.1716577404.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1724469622.1716577356; _ga_ZSF3D6YSLC=GS1.1.1716577356.1.1.1716577404.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': url,
        'locale': 'en',
        'tt': 'enZHdncy',
    }

    response = requests.post(
        'https://ssstik.io/abc',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data
    )
    soupe = BeautifulSoup(response. text, 'html.parser')
    download_link = soupe.a['href']
    response = requests.get(download_link, stream=True)
    with open('test.mp4', 'wb') as f:
        for chunk in response.iter_content(1024):
            if chunk:
                f.write(chunk)


bot = AsyncTeleBot(token=settings.BOT_TOKEN)
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

bot.setup_middleware(CustomMiddleware())
bot.setup_middleware(AntifloodMiddleware(bot=bot, limit=2.0))


@bot.message_handler(commands=['start'])
async def start_bot(message: Message) -> Message:
    """Обработчик команды start."""
    username = message.from_user.username
    language_code = await get_language_code(message)
    text = messages['start_message'][language_code].format(username)
    await bot.reply_to(message=message, text=text)


@bot.message_handler(commands=['help'])
async def help(message: Message) -> Message:
    """Обработчик команды help."""
    text = messages['help_msg']['rus']
    await bot.reply_to(message=message, text=text)


@bot.message_handler(commands=['statistics'])
async def statistics(message: Message) -> Message:
    """Обработчик команды statistics."""
    text = 'Стастистика загрузок'
    await bot.reply_to(message=message, text=text)


@bot.message_handler(commands=['language'])
async def language(message: Message) -> Message:
    """Обработчик команды /language для выбора языка."""
    text = 'Please, select a language:'
    markup = types.InlineKeyboardMarkup()
    button_rus = types.InlineKeyboardButton(
        'Русский 🇷🇺', callback_data='rus'
    )
    button_eng = types.InlineKeyboardButton(
        'English 🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data='eng'
    )
    markup.row(button_rus, button_eng)
    await bot.send_message(
        chat_id=message.chat.id, text=text, reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'save_music')
async def music_download(call: types.CallbackQuery):
    user_id = call.message.from_user.id
    video_name = mpy.VideoFileClip(call.message.video.file_name)
    music = video_name.audio
    mp4_file = "test.mp4"
    (
        ffmpeg
        .input("pipe:")
        .output(mp4_file, format="wav")
        .run_async()
    ).stdin(music)
    # music.write_arma(
    #     filename="music.mp3", fps=44100, bitrate=128000
    # )
    await bot.send_audio(
        chat_id=user_id,
        video=music,
        caption='@pq_downloader_bot',
    )


@bot.callback_query_handler(func=lambda call: True)
# @bot.callback_query_handler(func=lambda call: call.data == 'rus')
async def handle(call: types.CallbackQuery):
    language_code = await set_language_code(call.message, call.data)
    text = messages['set_language'][language_code]
    await bot.send_message(
        chat_id=call.message.chat.id, text=text
    )


@bot.message_handler()
async def video_download(message: Message):
    # message.from_user.language_code
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Скачать музыку', callback_data='save_music'
    ))
    markup.add(types.InlineKeyboardButton(
        'Убрать ограничение', callback_data='del_limit'
    ))
    get_video(message)
    user_id = message.from_user.id

    await bot.send_message(chat_id=user_id, text='Загрузка видео...')

    with open('test.mp4', 'rb') as video:
        await bot.send_video(
            chat_id=user_id,
            video=video,
            caption='@pq_downloader_bot',
            reply_markup=markup
        )
