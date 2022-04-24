import os

from flask import Flask, request
import logging
import json
from smapi import Client
import datetime as dt

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
    global token
    token = ''
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    global future_date
    future_date = dt.date.today() + dt.timedelta(days=1)

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я Алиса и я научилась работать с школьным порталом. Для начала работы ' \
                                  'разрешите мне просматривать ваш ШП ' \
                                  'Для этого перейдите по ссылке: https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=' \
                                  'После того, как дадите разрешение, скопируйте ссылку страницы, на которую вас перенаправили и отправьте её мне:)'

        res['response']['tts'] = 'Привет! Я Алиса и я науч+илась работать с школьным порталом. Для начала раб+оты ' \
                                 'разрешите мне просматривать ваш ШП. Для этого перейдите по ссылке.'

        return

    if 'https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id' in req['request'][
        'original_utterance']:
        # Пользователь согласился, прощаемся.
        token = req['request']['original_utterance'][255:-7]
        res['response']['text'] = 'Спасибо, доступ предоставлен, теперь я могу сообщать Вам оценки' \
                                  f'Ваш токен: {token}'
        return

    if req['request']['original_utterance'] in "домашнее задание на завтра" or "домашка":
        client = Client('OfN4nuja4zabUX3S0v5Hv3i2f28TnqQn')

        ans1 = dict(sorted(client.my_homeworks(future_date).items(), key=lambda f: int(f[0])))
        res['response']['text'] = ' '.join(list(ans1.values()))
        return

    if req['request']['original_utterance'] in "расписание на завтра" or "расписание":
        client = Client("r8eDzp0Vp645u89rzbjaiHOAd8eoMPSy")
        ans1 = dict(sorted(client.my_homeworks(future_date).items(), key=lambda f: int(f[0])))
        answer_full = ""
        for elem in ans1.values():
            answer_full += f'{(elem.split(":")[0])}\n'
        res['response']['text'] = answer_full
        return


    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = \
        f"Спросите что-нибудь полегче"
    res['response']['end_session'] = True
    return


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
