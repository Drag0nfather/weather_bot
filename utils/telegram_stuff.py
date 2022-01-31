import os
import sqlite3
from threading import Thread

import datetime
import schedule
import telebot
from dotenv import load_dotenv
from telebot import types

from coordinates_stuff import (get_coordinates_by_city,
                               split_coordinates_to_dict)

from text import create_output_message
from weather import YandexWeatherConnector, weather_api_key

CURRENT_HOUR = 0
dict_of_times = {}
dict_of_cities = {}
load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('CHAT_ID')
bot_client = telebot.TeleBot(token=telegram_token)
conn = sqlite3.connect('../db/weather.sqlite', check_same_thread=False)
cursor = conn.cursor()


def create_user_in_db(user_id, username):
    try:
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
    except:
        pass


def add_coordinates_to_db(user_id, coordinates):
    try:
        cursor.execute(f'UPDATE users SET user_coordinates = ? WHERE user_id LIKE ?', (str(coordinates), user_id))
        conn.commit()
    except:
        pass


def add_time_to_db(user_id, time_list):
    try:
        for i in range(0, 24):
            cursor.execute(f'UPDATE users SET time{i} = {0} WHERE user_id LIKE {user_id}')
            conn.commit()
        for time_elem in time_list:
            cursor.execute(f'UPDATE users SET time{time_elem} = {1} WHERE user_id LIKE {user_id}')
            conn.commit()
    except:
        pass


# def send_message(message, bot):
#     return bot.send_message(
#         chat_id=chat_id,
#         text=message
#     )


@bot_client.message_handler(commands=['start'])
def start_command(message):
    us_id = message.from_user.id
    username = message.from_user.username or 'NONE'
    create_user_in_db(user_id=us_id, username=username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    notification_button = types.KeyboardButton('Уведомления')
    get_weather_button = types.KeyboardButton('Получить информацию о погоде')
    markup.add(get_weather_button, notification_button)
    bot_client.send_message(
        message.chat.id,
        "Привет, с Вами на связи погодный бот! Я умею отправлять уведомление о погоде в заданное время",
        reply_markup=markup
    )


@bot_client.message_handler(content_types=['text'])
def get_text_message(message):
    user_id = message.chat.id
    if message.text == 'Получить информацию о погоде':
        get_weather_method(message)
    if message.text == 'Назад':
        main_menu(message)
    if message.text == 'Уведомления':
        notification(message)
    if message.text == 'Ввести город':
        output_weather_by_text(message)
    if message.text == 'Отправить геопозицию':
        output_weather_by_geo(message)
    if message.text == 'Назад к выбору времени':
        notification(message)
    if message.text == 'Назад к способу выбора погоды':
        get_weather_method(message)
    if message.text == 'Назад в главное меню':
        if user_id in dict_of_times:
            dict_of_times.pop(user_id)
        main_menu(message)


@bot_client.message_handler(content_types=['text'])
def get_text_message_and_add_to_db(message):
    if message.text == 'Введите город':
        output_weather_by_text_and_add_to_db(message)
    if message.text == 'Отправьте геопозицию':
        output_weather_by_geo_and_add_to_db(message)
    if message.text == 'Вернуться к способу выбора погоды':
        get_weather_method_and_add_to_db(message)


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    notification_button = types.KeyboardButton('Уведомления')
    get_weather_button = types.KeyboardButton('Получить информацию о погоде')
    markup.add(get_weather_button, notification_button)
    bot_client.send_message(
        message.chat.id,
        'Вы в главном меню',
        reply_markup=markup
    )


def output_weather_by_text(message):
    if message.text == 'Назад к способу выбора погоды':
        bot_client.register_next_step_handler(message, get_text_message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton('Назад к способу выбора погоды')
    back_to_menu_button = types.KeyboardButton('Назад в главное меню')
    markup.add(back_to_menu_button, back_button)
    bot_client.send_message(
        message.chat.id,
        f'Введите город',
        reply_markup=markup
    )
    bot_client.register_next_step_handler(message, get_client_city)


def output_weather_by_text_and_add_to_db(message):
    if message.text == 'Вернуться к способу выбора погоды':
        bot_client.register_next_step_handler(message, get_text_message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton('Вернуться к способу выбора погоды')
    back_to_menu_button = types.KeyboardButton('Назад в главное меню')
    markup.add(back_to_menu_button, back_button)
    bot_client.send_message(
        message.chat.id,
        f'Введите город',
        reply_markup=markup
    )
    bot_client.register_next_step_handler(message, get_client_city_and_add_to_db)


@bot_client.message_handler(content_types=['text'])
def get_client_city(message):
    if message.text == 'Назад':
        main_menu(message)
    elif message.text == 'Назад в главное меню':
        bot_client.register_next_step_handler(message, get_text_message)
        main_menu(message)
    elif message.text == 'Ввести город':
        pass
    elif message.text == 'Введите город':
        pass
        bot_client.register_next_step_handler(message, get_client_city)
    elif message.text == 'Назад к способу выбора погоды':
        bot_client.register_next_step_handler(message, get_text_message)
        get_weather_method(message)
    else:
        try:
            client_city = message.text
            coordinates = get_coordinates_by_city(client_city)
            dict_coordinates = split_coordinates_to_dict(coordinates)
            weather = YandexWeatherConnector(token=weather_api_key)
            weather_stuff = weather.get_weather_by_cors(dict_coordinates)
            output_message = create_output_message(weather_stuff)
            bot_client.send_message(message.from_user.id, output_message)
            bot_client.register_next_step_handler(message, get_client_city)
        except:
            bot_client.send_message(message.from_user.id, 'Город не найден, попробуй еще раз')
            bot_client.register_next_step_handler(message, get_client_city)


@bot_client.message_handler(content_types=['text'])
def get_client_city_and_add_to_db(message):
    if message.text == 'Назад':
        output_weather_by_text_and_add_to_db(message)
    elif message.text == 'Назад в главное меню':
        bot_client.register_next_step_handler(message, get_text_message)
        main_menu(message)
    elif message.text == 'Ввести город':
        pass
    elif message.text == 'Введите город':
        pass
        bot_client.register_next_step_handler(message, get_client_city_and_add_to_db)
    elif message.text == 'Назад к способу выбора погоды':
        bot_client.register_next_step_handler(message, get_text_message_and_add_to_db)
        get_weather_method_and_add_to_db(message)
    else:
        try:
            client_city = message.text
            user_id = message.from_user.id
            coordinates = get_coordinates_by_city(client_city)
            dict_of_cities[user_id] = f'({coordinates})'
            confirm_user_city(message, client_city)
            bot_client.register_next_step_handler(message, confirm_user_city_handler)
        except:
            bot_client.send_message(message.from_user.id, 'Город не найден, попробуй еще раз')
            bot_client.register_next_step_handler(message, get_client_city_and_add_to_db)


def confirm_user_city(message, city):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.KeyboardButton('Да')
    decline_button = types.KeyboardButton('Нет')
    markup.add(confirm_button, decline_button)
    bot_client.send_message(
        message.chat.id,
        f'Подтверждаете отправку погоды в городе {city}?',
        reply_markup=markup
    )


@bot_client.message_handler(content_types=['text'])
def confirm_user_city_handler(message):
    if message.text == 'Да':
        user_id = message.from_user.id
        coordinates = dict_of_cities[user_id]
        add_coordinates_to_db(user_id, coordinates)
        dict_of_cities.pop(user_id)
        dict_of_times.pop(user_id)
        main_menu(message)
        bot_client.register_next_step_handler(message, get_text_message)
    if message.text == 'Нет':
        output_weather_by_text_and_add_to_db(message)
        bot_client.register_next_step_handler(message, get_client_city_and_add_to_db)
    else:
        pass


def get_weather_method(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    city_by_input_button = types.KeyboardButton('Ввести город')
    city_by_geo_button = types.KeyboardButton('Отправить геопозицию')
    markup.add(city_by_input_button, city_by_geo_button, back_button)
    bot_client.send_message(
        message.chat.id,
        'Вы можете либо ввести город вручную, либо отправить геопозицию',
        reply_markup=markup
    )


def get_weather_method_and_add_to_db(message, add_to_db=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_time_button = types.KeyboardButton('Назад к выбору времени')
    city_by_input_button = types.KeyboardButton('Введите город')
    city_by_geo_button = types.KeyboardButton('Отправьте геопозицию')
    markup.add(city_by_input_button, city_by_geo_button, back_to_time_button)
    back_to_menu_button = types.KeyboardButton('Назад в главное меню')
    markup.add(back_to_menu_button)
    bot_client.send_message(
        message.chat.id,
        'Чтобы установить время выберите город вручную, либо отправьте местоположение',
        reply_markup=markup
    )
    bot_client.register_next_step_handler(message, get_text_message_and_add_to_db)


def output_weather_by_geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    back_button = types.KeyboardButton('Назад к способу выбора погоды')
    back_to_menu_button = types.KeyboardButton('Назад в главное меню')
    keyboard.add(button_geo)
    keyboard.add(back_to_menu_button, back_button)

    bot_client.send_message(message.chat.id, "Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)


def output_weather_by_geo_and_add_to_db(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    back_button = types.KeyboardButton('Вернуться к способу выбора погоды')
    back_to_menu_button = types.KeyboardButton('Назад в главное меню')
    keyboard.add(button_geo)
    keyboard.add(back_to_menu_button, back_button)
    bot_client.register_next_step_handler(message, location_and_add_to_db)
    bot_client.send_message(message.chat.id, "Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)


def send_weather_by_coordinates(message, coordinates):
    if message.text == 'Назад':
        main_menu(message)
    else:
        try:
            dict_coordinates = split_coordinates_to_dict(coordinates, flag=True)
            weather = YandexWeatherConnector(token=weather_api_key)
            weather_stuff = weather.get_weather_by_cors(dict_coordinates)
            output_message = create_output_message(weather_stuff)
            bot_client.send_message(message.from_user.id, output_message)
            bot_client.register_next_step_handler(message, get_client_city)
        except:
            bot_client.send_message(message.from_user.id, 'Город не найден, попробуй еще раз')
            bot_client.register_next_step_handler(message, get_client_city)


def send_weather_by_coordinates_and_add_to_db(message, coordinates):
    if message.text == 'Назад':
        main_menu(message)
    else:
        try:
            dict_coordinates = split_coordinates_to_dict(coordinates, flag=True)
            weather = YandexWeatherConnector(token=weather_api_key)
            weather_stuff = weather.get_weather_by_cors(dict_coordinates)
            output_message = create_output_message(weather_stuff)
            bot_client.send_message(message.from_user.id, output_message)
            bot_client.register_next_step_handler(message, get_client_city)
        except:
            bot_client.send_message(message.from_user.id, 'Город не найден, попробуй еще раз')
            bot_client.register_next_step_handler(message, get_client_city)


@bot_client.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        coordinates = (message.location.latitude, message.location.longitude)
        send_weather_by_coordinates(message, coordinates)


@bot_client.message_handler(content_types=["location"])
def location_and_add_to_db(message):
    if message.location is not None:
        user_id = message.from_user.id
        coordinates = (message.location.latitude, message.location.longitude)
        add_coordinates_to_db(user_id, coordinates)
        dict_of_times.pop(user_id)
        main_menu(message)
        bot_client.register_next_step_handler(message, get_text_message)


def notification(message, flag=False, ):
    a = [i for i in range(24)]
    key = types.InlineKeyboardMarkup(row_width=4)
    buttons = []
    user_id = message.chat.id
    for i in range(len(a)):
        if user_id not in dict_of_times.keys():
            buttons.append(
                types.InlineKeyboardButton(text=f'{a[i]}:00', callback_data=str(a[i])))
        else:
            if a[i] in dict_of_times[user_id]:
                buttons.append(
                    types.InlineKeyboardButton(text=f'✅{a[i]}:00', callback_data=f'✅{a[i]}'))
            else:
                buttons.append(
                    types.InlineKeyboardButton(text=f'{a[i]}:00', callback_data=str(a[i])))
    back_button = types.InlineKeyboardButton(text='Перейти к выбору города', callback_data='Перейти к выбору города')
    key.add(*buttons)
    key.add(back_button)
    if flag is False:
        bot_client.send_message(
            message.chat.id, 'Выберите часы', reply_markup=key
        )
    else:
        bot_client.delete_message(
            message.chat.id, message.id)
        bot_client.send_message(
            message.chat.id, 'Выберите часы', reply_markup=key
        )


@bot_client.callback_query_handler(func=lambda c: True)
def callback_inline(call):
    """
    Функция обработки инлайновых кнопок
    """
    if call.message:
        user_id = call.from_user.id
        if call.data == 'Перейти к выбору города':
            if user_id in dict_of_times:
                list_of_times = dict_of_times[user_id]
                list_of_times.sort()
                add_time_to_db(user_id, list_of_times)

                # remove inline buttons
                bot_client.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Выберите город, в котором хотите получать погоду",
                    reply_markup=None
                )
                get_weather_method_and_add_to_db(call.message)
            else:
                bot_client.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Вы не добавили время :(",
                    reply_markup=None
                )
                main_menu(call.message)
        if call.data[0].isdigit() and user_id not in dict_of_times.keys():
            dict_of_times[user_id] = [int(call.data)]
            bot_client.edit_message_reply_markup(
                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=notification(
                    call.message, flag=True)
            )
            print(dict_of_times)
        elif call.data[0].isdigit() and user_id in dict_of_times.keys():
            if int(call.data) not in dict_of_times[user_id]:
                dict_of_times[user_id].append(int(call.data))
                bot_client.edit_message_reply_markup(
                    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=notification(
                        call.message, flag=True)
                )
                print(dict_of_times)
        if call.data.startswith('✅'):
            time_str = call.data[1:]
            dict_of_times[user_id].remove(int(time_str))
            bot_client.edit_message_reply_markup(
                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=notification(
                    call.message, flag=True)
            )


def time_checker():
    curr_hour = datetime.datetime.now().hour
    global CURRENT_HOUR, output_message
    if curr_hour != CURRENT_HOUR:
        cursor.execute(f'SELECT user_id, user_coordinates FROM users WHERE time{curr_hour} LIKE 1')
        users_list_to_send_msg = cursor.fetchall()
        for user, user_coordinates in users_list_to_send_msg:
            try:
                lat, lon = user_coordinates[1:-1].split(',')
                dict_coordinates = {
                    'lat': lat,
                    'lon': lon
                }
                weather = YandexWeatherConnector(token=weather_api_key)
                weather_stuff = weather.get_weather_by_cors(dict_coordinates)
                output_message = create_output_message(weather_stuff)
            except:
                print(f'weather for user {user} and coordinates {user_coordinates[0]} not found')
                pass
            try:
                bot_client.send_message(user, output_message)
            except:
                print(f'user {user} not found')
                pass
        CURRENT_HOUR = curr_hour


def scheduler():
    schedule.every().second.do(time_checker)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    thread = Thread(target=scheduler)
    thread.start()
    bot_client.polling(none_stop=True, interval=0)
