from telebot import BaseMiddleware, CancelUpdate

from bot.services import update_or_create_user
from telebot import types


class CustomMiddleware(BaseMiddleware):

    def __init__(self):

        super(CustomMiddleware, self).__init__()
        self.update_sensitive = True
        self.update_types = ['message']

    async def pre_process_message(self, message, data):
        """Only message update here."""
        my_data = None
        try:
            my_data = getattr(message, 'chat')
        except AttributeError:
            pass
        try:
            my_data = getattr(message, 'from_user')
        except AttributeError:
            pass
        if not my_data:
            return None
        if not message.text:
            return None
        await update_or_create_user(my_data)

    async def post_process_message(self, message, data, exception):
        """Only message update here for post_process."""
        pass

    async def pre_process_edited_message(self, message, data):
        """Only edited_message update here."""
        pass

    async def post_process_edited_message(self, message, data, exception):
        """Only edited_message update here for post_process."""
        pass


class AntifloodMiddleware(BaseMiddleware):

    def __init__(self, bot, limit: float) -> None:
        self.bot = bot
        self.last_time: dict = {}
        self.limit: float = limit
        self.update_types: list = ['message']

    async def pre_process(self, message: types.Message, data):
        if message.from_user.id not in self.last_time:
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            await self.bot.send_message(
                message.chat.id, 'You are sending messages too often!'
            )
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    async def post_process(self, message, data, exception):
        pass
