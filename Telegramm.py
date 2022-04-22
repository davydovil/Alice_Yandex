import datetime
import telebot
from smapi import Client

bot = telebot.TeleBot('5368830125:AAGn7jwS_GogvE7kCsEuICalF2UYnlMBCZQ')
token = 0

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Разрешите мне просматривать ваш Школьный портал. Для этого перейдите по ссылке")
        bot.send_message(message.from_user.id,
                         "https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=")
        bot.send_message(message.from_user.id,
                         "После скопируйте адрес страниц, на которую вас перенаправят и отправьте в виде сообщения")
    elif "https://login.school.mosreg.ru/oauth2/Authorization/Result?response_type=token&client_id" in message.text:
        token = message.text[255:-7]
        bot.send_message(message.from_user.id, f"доступ предоставлен, приятного использования. Ваш токен - {token}")
    elif message.text.lower() == "домашнее задание на завтра" and token != 0:
        client = Client(token)
        bot.send_message(message.from_user.id, client.my_homeworks(datetime.date.today() + datetime.timedelta(days=1)))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
