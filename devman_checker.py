import requests
import time

from requests.exceptions import ReadTimeout, ConnectionError
from telegram_bot import send_message


def get_lp_checklist(token, timestamp=None):
    url = 'https://dvmn.org/api/long_polling//'
    headers = {'Authorization': f'Token {token}'}
    payload = {'timestamp': timestamp}
    response = requests.get(url=url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def poll_dvmn(dvmn_token, bot_token, chat_id, timestamp):
    response = get_lp_checklist(dvmn_token, timestamp)
    if response['status'] == 'found':
        text=parse_found_response(response['new_attempts'][0])
        send_message(bot_token=bot_token, chat_id=chat_id, text=text)
        timestamp = response['new_attempts'][0]['timestamp']
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



def run_checker(dvmn_token, bot_token, chat_id):    
    timestamp = None
    while True:
        try:
            timestamp = poll_dvmn(dvmn_token, bot_token, chat_id, timestamp)
        except ReadTimeout:
            continue
        except ConnectionError:
            time.sleep(60)
            continue