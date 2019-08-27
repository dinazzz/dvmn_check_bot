import os
import logging

from devman_checker import run_checker


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    DVMN_TOKEN = os.getenv('DVMN_TOKEN')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('chat_id')
    run_checker(DVMN_TOKEN, TELEGRAM_BOT_TOKEN, chat_id)