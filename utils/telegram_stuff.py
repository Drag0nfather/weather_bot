import telebot
from telebot import types
import os
from coordinates_stuff import get_coordinates_by_city, split_coordinates_to_dict
from text import create_output_message
from weather import YandexWeatherConnector, weather_api_key
from dotenv import load_dotenv


load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('CHAT_ID')
bot_client = telebot.TeleBot(token=telegram_token)


def send_message(message, bot_client):
    return bot_client.send_message(
        chat_id=chat_id,
        text=message
    )


@bot_client.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    notification_button = types.KeyboardButton('Уведомления')
    get_weather_button = types.KeyboardButton('Получить информацию о погоде')
    markup.add(get_weather_button, notification_button, )
    bot_client.send_message(
        message.chat.id,
        ("Привет, с Вами на связи погодный бот! Я умею отправлять уведомление"
         "о погоде в заданное время"),
        reply_markup=markup
    )


def output_weather(message):
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        notification_button = types.KeyboardButton('Уведомления')
        get_weather_button = types.KeyboardButton('Получить информацию о погоде')
        markup.add(notification_button, get_weather_button)
        bot_client.send_message(
            message.chat.id,
            ("Вы в главном меню"), reply_markup=markup
        )
    else:
        try:
            client_city = message.text
            coordinates = get_coordinates_by_city(client_city)
            dict_coordinates = split_coordinates_to_dict(coordinates)
            weather = YandexWeatherConnector(token=weather_api_key)
            weather_stuff = weather.get_weather_by_cors(dict_coordinates)
            output_message = create_output_message(weather_stuff)
            bot_client.send_message(message.from_user.id, output_message)
            bot_client.register_next_step_handler(message, output_weather)
        except Exception:
            bot_client.send_message(message.from_user.id, 'Город не найден, попробуй еще раз')
            bot_client.register_next_step_handler(message, output_weather)


@bot_client.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Получить информацию о погоде':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('Назад')
        markup.add(back_button)
        bot_client.send_message(
            message.chat.id,
            f'Введите город',
            reply_markup=markup
        )
        bot_client.register_next_step_handler(message, output_weather)

    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        notification_button = types.KeyboardButton('Уведомления')
        get_weather_button = types.KeyboardButton('Получить информацию о погоде')
        markup.add(notification_button, get_weather_button)
        bot_client.send_message(
            message.chat.id,
            ("Вы в главном меню"),
            reply_markup=markup
        )


if __name__ == '__main__':
    bot_client.polling(none_stop=True, interval=0)
