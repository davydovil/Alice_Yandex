import json
import logging
import os

from flask import Flask, request
from smapi import Client

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    token = ''
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я Алиса и я научилась работать с школьным порталом. Для начала работы ' \
                                  'разрешите мне просматривать ваш ШП ' \
                                  'Для этого перейдите по ссылке: https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=' \
                                  'После того, как дадите разрешение, скопируйте ссылку страницы, на которую вас перенаправили и отправьте её мне:)'

        res['response']['tts'] = 'Привет! Я Алиса и я науч+илась работать с школьным порталом. Для начала раб+оты ' \
                                 'разрешите мне просматривать ваш ШП. Для этого перейдите по ссылке.'

        return

    if 'https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id' in req['request']['original_utterance']:
        # Пользователь авторизовался продолжаем общение.
        token = req['request']['original_utterance'][255:-7]
        res['response']['text'] = 'Спасибо, доступ предоставлен, теперь я могу сообщать Вам оценки' \
                                  f'Ваш токен: {token}'
        return

    if req['request']['original_utterance'].lower() in [
        'домашка',
        'домашка на завтра',
        'домашнее задание на завтра',
        'домашнее задание'
    ]:
        client = Client(token)
        res['response']['text'] = client.my_homeworks("2022-04-11 00:00:00", "2022-04-11 23:59:00")

    if req['request']['original_utterance'].lower() in [
        'оценки',
        'мои оценки',
        'мои оценки за сегодня',
        'что получил сегодня'
        ]:
        client = Client(token)       # Здесь токен пользователя(Илья)
        res['response']['text'] = client.get_person_marks_for_period("2022-04-11 00:00:00", "2022-04-11 23:59:00")

    if req['request']['original_utterance'].lower() in [
        'расписание',
        'уроки',
        'к какому '
        ]:
        client = Client(token)  # Здесь токен пользователя(Илья)
        res['response']['text'] = client.get_school_timetable("2022-04-11 00:00:00", "2022-04-11 23:59:00")

    res['response']['text'] = \
        f"Спросите что-нибудь полегче"
    res['response']['end_session'] = True
    return


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
