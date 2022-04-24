import os

from flask import Flask, request
import logging
import json
from smapi import Client
import datetime as dt
from database_toAlice import new_user, get_token

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    future_date = None
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    future_date = dt.date.today() + dt.timedelta(days=1)

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я научилась работать со школьным порталом. Предоставь мне к нему доступ' \
                                  'Для этого перейдите по ссылке:' \
                                  'После того, как дадите разрешение, скопируйте ссылку страницы,' \
                                  ' на которую вас перенаправили и отправьте её мне:)'
        res['response']['buttons'] = []
        reg_url_button = {'url': "https://catsee.ru/", 'title': 'Ссыль', 'hide': True}
        res['response']['buttons'].append(reg_url_button)

        res['response']['tts'] = 'Привет! Я научилась работать со школьным порталом. Предоставь мне к нему доступ ' \
                                 'Для этого перейдите по ссылке.'

        return res

    elif 'https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id' in \
            req['request']['original_utterance']:

        token = req['request']['original_utterance'][255:-7]
        new_user(user_id, token)
        res['response']['text'] = f'Спасибо, доступ предоставлен'
        return

    elif req['session']['new'] and get_token(user_id) == '':
        res['response']['text'] = 'Что тебе подсказать?'
        res['response']['buttons'] = []
        homework_button = {}
        homework_button['title'] = 'домашка'
        res['response']['buttons'].append(homework_button)
        b = {}
        b['title'] = 'расписание'
        res['response']['buttons'].append(b)
        return

    elif "домашнее задание на завтра" in req['request']['original_utterance'] or "домашка" in \
            req['request']['original_utterance'] and get_token(user_id) != '':
        client = Client(get_token(user_id))
        ans1 = dict(sorted(client.my_homeworks(future_date).items(), key=lambda f: int(f[0])))
        res['response']['text'] = ' '.join(list(ans1.values()))
        return

    else:
        res['response']['text'] = \
            f"Спросите что-нибудь полегче"
        return


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
