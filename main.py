import os
import logging

from devman_checker import run_checker, MyLogsHandler
from requests.exceptions import HTTPError


if __name__ == '__main__':
    DVMN_TOKEN = os.getenv('DVMN_TOKEN')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('chat_id')

    logging.basicConfig(level=logging.INFO, format='%(processName)s %(asctime)s %(message)s')
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(chat_id=chat_id, bot_token=TELEGRAM_BOT_TOKEN))
    logger.info('Тут сработало')
    try:
        run_checker(DVMN_TOKEN, TELEGRAM_BOT_TOKEN, chat_id, logger)
    except HTTPError as http_exc:
        logger.error('Бот упал!')
        logger.exception()
