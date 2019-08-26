import telegram


def send_message(bot_token, chat_id, text):
    bot = telegram.Bot(bot_token)
    bot.send_message(chat_id=chat_id, text=text)