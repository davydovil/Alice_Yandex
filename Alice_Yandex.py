import os

from flask import Flask, request
import logging
import json

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
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я Алиса и я научилась работать с школьным порталом. Для начала работы ' \
                                  'разрешите мне просматривать ваш ШП '
        res['response']['tts'] = 'Привет! Я Алиса и я науч+илась работать с школьным порталом. Для начала раб+оты ' \
                                 'разрешите мне просматривать ваш ШП '

        return

    if req['request']['original_utterance'].lower() in [
        'сколько задали на понедельник'
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Я пока не умею смотреть ДЗ, но это не на долго'
        res['response']['end_session'] = True
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = \
        f"Спросите что-нибудь полегче"
    res['response']['end_session'] = True
    return


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
