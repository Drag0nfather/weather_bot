import telebot
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
    bot_client.send_message(
        message.chat.id,
        ("Привет, с Вами на связи погодный бот! "
         "Чтобы начать получать погоду введи свой город в чат")
    )


@bot_client.message_handler(content_types=['text'])
def get_text_message(message):
    client_city = message.text
    try:
        coordinates = get_coordinates_by_city(client_city)
        dict_coordinates = split_coordinates_to_dict(coordinates)
        weather = YandexWeatherConnector(token=weather_api_key)
        weather_stuff = weather.get_weather_by_cors(dict_coordinates)
        output_message = create_output_message(weather_stuff)
        bot_client.send_message(message.from_user.id, output_message)
    except Exception:
        bot_client.send_message(message.from_user.id, 'Город не найден, попробуй еще раз')


if __name__ == '__main__':
    bot_client.polling(none_stop=True, interval=0)
