from telebot import BaseMiddleware

from bot.services import update_or_create_user


class CustomMiddleware(BaseMiddleware):

    def __init__(self):

        super(CustomMiddleware, self).__init__()
        self.update_sensitive = True
        self.update_types = ['message']

    async def pre_process_message(self, message, data):
        # only message update here
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
        # only message update here for post_process
        pass

    async def pre_process_edited_message(self, message, data):
        # only edited_message update here
        pass

    async def post_process_edited_message(self, message, data, exception):
        # only edited_message update here for post_process
        pass
