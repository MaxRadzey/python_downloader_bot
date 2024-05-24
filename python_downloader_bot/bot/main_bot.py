import logging
import requests
from bs4 import BeautifulSoup

from telebot.async_telebot import AsyncTeleBot
import telebot

from django.conf import settings


# url = 'https://www.tiktok.com/@_il9_/video/7043465037918326018'
# TikTok URL https://www.tiktok.com/@_il9_/video/7043465037918326018


def get_video(url):
    # response = requests.get(url, stream=True)
    # page = BeautifulSoup(response.content, 'html.parser')

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

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
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


def get_tiktok_url(url: str) -> str | None:
    if '.tiktok.com' in url:
        return url
    return None


@bot.message_handler(commands=['start'])
async def start_bot(message):
    """Обработчик команды start."""
    text = 'Hi, I am TikTok Downloader Bot.\nSend me url!'
    await bot.reply_to(message=message, text=text)


@bot.message_handler(commands=['help'])
async def help(message):
    """Обработчик команды help."""
    text = 'Some text HELP!!'
    await bot.reply_to(message=message, text=text)


@bot.message_handler()
async def video_download(message):
    get_video(message)
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text='Загрузка видео...')
    with open('test.mp4', 'rb') as video:
        print('aaaa')
        await bot.send_video(chat_id=user_id, video=video, caption='@pq_downloader_bot')

# @bot.message_handler(func=lambda message: True)
# async def echo_message(message):
#     user_id = message.from_user.id
#     full_name = message.from_user.full_name
#     username = message.from_user.username
#     text = message.text
#     url = get_tiktok_url(text)
#     if url:
#         ...
#     logger.info(f'{user_id=}')
#     logger.info(f'{full_name=}')
#     logger.info(f'{username=}')
#     logger.info(f'{text=}')
#     await bot.reply_to(message=message, text=message.text)
    # await bot.send_video(chat_id=user_id, video=..., caption=...,)
