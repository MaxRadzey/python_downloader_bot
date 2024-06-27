# TikTok Downloader Bot

## Содержание
- [Авторы](#авторы)
- [Описание](#описание)
- [Технологии](#технологии)
- [Как запустить проект](#Как-запустить-проект)

##  Авторы

- [Maxim Radzey](https://github.com/MaxRadzey)

##  Описание
Бот для загрузки видео из ТикТока через телеграм бота без вотермарок по ссылке, также есть возможность загрузки музыки из видео для дальнейшего использования в своих проектах.
Реализована админка на джанго для управления пользователями, количеством скачанных видео и их статусом. Также реализовано сохранение данных в БД SQlite.

## Технологии
- [Django](https://docs.djangoproject.com/en/stable/)
- [Python 3.11](https://www.python.org)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

### Как запустить проект:

Клонировать репозиторий:

```
git@github.com:MaxRadzey/foodgram-project-react.git
```

Создать файл .env и указать актуальные данные

```
BOT_TOKEN= Токе ТГ бота
LOG_LEVEL=INFO
TELEGRAM_ID_ADMIN= Айди админа в телеграме

DEBUG=True
SECRET_KEY = Секретный ключ джанго-проекта
ALLOWED_HOSTS='*'
```
Бот запускается командой
```
python manage.py run_bot
```
