import requests
import time
import logging
import telegram

from requests.exceptions import ReadTimeout, ConnectionError


class MyLogsHandler(logging.Handler):

    def __init__(self, bot_token, chat_id):
        logging.Handler.__init__(self)
        self.bot = telegram.Bot(bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(bot_token, chat_id, text):
    bot = telegram.Bot(bot_token)
    bot.send_message(chat_id=chat_id, text=text)


def get_lp_checklist(token, timestamp=None):
    url = r'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {token}'}
    payload = {'timestamp': timestamp}
    response = requests.get(url=url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def poll_dvmn(dvmn_token, bot_token, chat_id, timestamp):
    response = get_lp_checklist(dvmn_token, timestamp)
    if response['status'] == 'found':
        for attempt in response['new_attempts']:
            text=parse_found_response(attempt)
            send_message(bot_token=bot_token, chat_id=chat_id, text=text)
        timestamp = response['last_attempt_timestamp']
    else:
        timestamp = response['timestamp_to_request']
    return timestamp


def parse_found_response(check_results):
    lesson_title = check_results['lesson_title']
    if check_results['is_negative']:
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Преподавателю всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{lesson_title}"!\n\n{verdict}'


def run_checker(dvmn_token, bot_token, chat_id, logger):
    logger.info('Бот запущен')
    timestamp = None
    while True:
        try:
            a =0/0
            timestamp = poll_dvmn(dvmn_token, bot_token, chat_id, timestamp)
        except ReadTimeout as timeout_exc:
            logger.exception(timeout_exc)
            continue
        except ConnectionError as connection_exc:
            logger.exception(connection_exc)
            time.sleep(300)
            continue
        except ZeroDivisionError as zero_div_exc:
            logger.exception(zero_div_exc)
            time.sleep(20000)
            continue



