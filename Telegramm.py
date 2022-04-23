import datetime
import telebot
from smapi import Client
from WorkingWithDB_telegram import get_token, new_user

bot = telebot.TeleBot('5368830125:AAGn7jwS_GogvE7kCsEuICalF2UYnlMBCZQ')


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        user_id = message.from_user.id
        if get_token(user_id):
            bot.send_message(message.from_user.id, 'Доступ предоставлен')
        else:
            bot.send_message(message.from_user.id,
                             "Разрешите мне просматривать ваш Школьный портал. Для этого перейдите по ссылке")
            bot.send_message(message.from_user.id,
                             "https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=")
            bot.send_message(message.from_user.id,
                             "После скопируйте адрес страниц, на которую вас перенаправят и отправьте в виде сообщения")
    elif "https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id" in message.text:
        token = message.text[255:-7]
        user_id = message.from_user.id
        new_user(user_id, token)
        client = Client(token)
        bot.send_message(message.from_user.id,
                         f"доступ предоставлен {client.get_me()['name']}, приятного использования. Ваш токен - {token}")
    elif message.text.lower() == "домашнее задание" or message.text.lower() == "/homework":
        client = Client(get_token(message.from_user.id)[0][0])
        if datetime.date.today().weekday() == 6 or datetime.date.today().weekday() == 7:
            gg = client.my_homeworks(datetime.date.today() + datetime.timedelta(days=3))
            for i in sorted(gg.keys()):
                bot.send_message(message.from_user.id, f"{i} урок: {gg[i]}")
    elif message.text.lower() == 'оценки':
        client = Client(get_token(message.from_user.id)[0][0])
        if datetime.date.today().weekday() == 6 or datetime.date.today().weekday() == 7:
            gg = client.my_marks(str(datetime.date.today() - datetime.timedelta(days=6)))
            for i in sorted(gg.keys()):
                bot.send_message(message.from_user.id, f"{i} урок: {gg[i]}")
        else:
            gg = client.my_marks(str(datetime.date.today()))
            for i in sorted(gg.keys()):
                bot.send_message(message.from_user.id, f"{i} урок: {gg[i]}")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
