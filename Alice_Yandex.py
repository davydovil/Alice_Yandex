import os

from flask import Flask, request
import logging
import json
from smapi import Client
import datetime
from database_toAlice import new_user, get_token

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    token = ''
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response, token)

    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res, token):
    user_id = req['session']['user_id']

    if req['session']['new'] and token == '':
        res['response']['text'] = 'Разрешите мне просматривать ваш Школьный портал ' \
                                  'https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=' \
                                  'После скопируйте адрес страницы этой страницы'

        res['response']['tts'] = 'Разрешите мне просматривать ваш Школьный портал. Перейдите по ссылке' \
                                 'и После скопируйте адрес этой страницы'

        if 'https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id' in req['request'][
            'original_utterance']:
            token = req['request']['original_utterance'][255:-7]
            new_user(user_id, token)
            res['response']['text'] = 'Доступ предоставлен.'
            return
    elif req['session']['new'] and token != '':
        res['response']['text'] = 'Что вам подсказать?'
        return

    if 'домашнее задание на завтра' in req['request']['original_utterance'] and get_token(user_id):
        client = Client(get_token(user_id))
        res['response']['text'] = client.my_homeworks(datetime.date.today() + datetime.timedelta(days=1))
        return
    else:
        res['response']['text'] = 'Разрешите мне просматривать ваш Школьный портал ' \
                                 'https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=' \
                                 'После скопируйте адрес страницы этой страницы'

        res['response']['tts'] = 'Разрешите мне просматривать ваш Школьный портал. Перейдите по ссылке' \
                                 'и После скопируйте адрес этой страницы'

        if 'https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id' in req['request'][
            'original_utterance']:
            token = req['request']['original_utterance'][255:-7]
            new_user(user_id, token)
            res['response']['text'] = 'Доступ предоставлен.'
            return

    res['response']['text'] = \
        f"Спросите что-нибудь полегче"
    res['response']['end_session'] = True
    return


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
