import telebot
import requests
import json
import buttons15_2 as bt
import database15_2 as db

bot = telebot.TeleBot('7870136037:AAE8W0Dl2DkLQUEEBIAvgNlkprFH0WqhqDM')
weather_api = 'e8c495b8ac3061540139b4e8eff25c25'


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Выберите язык/Tilni tanlang', reply_markup=bt.choose_lang())
    bot.register_next_step_handler(message, lang)


def lang(message):
    user_id = message.from_user.id
    if message.text.lower() == 'ru':
        bot.send_message(user_id, 'Вы выбрали русский язык', reply_markup=bt.cont_ru())
        bot.register_next_step_handler(message, register_ru)
    elif message.text.lower() == 'uz':
        bot.send_message(user_id, 'Siz ozbek tilini tanlagansiz', reply_markup=bt.cont_uz())
        bot.register_next_step_handler(message, register_uz)


def register_ru(message):
    user_id = message.from_user.id
    name = db.get_username(user_id)
    if db.check_user(user_id):
        bot.send_message(user_id, f'Добро пожаловать {name}!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Давайте начнем регистрацию!\n'
                                  'Введите ваше Имя!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name_ru)


def register_uz(message):
    user_id = message.from_user.id
    name = db.get_username(user_id)
    if db.check_user(user_id):
        bot.send_message(user_id, f'Xush kelibsiz {name}!')
    else:
        bot.send_message(user_id, 'Salom! Royxatdan otishni boshlaymiz!\n'
                                  'Ismingizni kiriting!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name_uz)


def get_name_ru(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, f'Отлично {user_name}! Теперь отправьте свой номер через кнопку!', reply_markup=bt.number_button_ru())
    bot.register_next_step_handler(message, get_number_ru, user_name)


def get_name_uz(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, f'Ajoyib {user_name}! Endi tugma orqali raqamingizni yuboring!', reply_markup=bt.number_button_uz())
    bot.register_next_step_handler(message, get_number_uz, user_name)


def get_number_ru(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        db.register(user_id, user_name, user_number)
        bot.send_message(user_id, 'Вы успешно зарегистрированы! Теперь отправьте свою локацию через кнопку!', reply_markup=bt.location_button_ru())
        bot.register_next_step_handler(message, get_location_ru, user_name)
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку ниже!')
        bot.register_next_step_handler(message, get_number_ru, user_name)


def get_number_uz(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        db.register(user_id, user_name, user_number)
        bot.send_message(user_id, 'Siz royxatdan otdingiz! Endi tugma orqali joylashuvingizni yuboring!', reply_markup=bt.location_button_uz())
        bot.register_next_step_handler(message, get_location_uz, user_name)
    else:
        bot.send_message(user_id, 'Quyidagi tugma orqali raqamingizni yuboring!')
        bot.register_next_step_handler(message, get_number_uz, user_name)


def get_location_ru(message, user_name):
    user_id = message.from_user.id
    if message.location:
        loc = message.location
        db.register_loc(user_id, loc.latitude, loc.longitude)
        bot.send_message(user_id, 'Вы успешно зарегистрированы!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку ниже!')
        bot.register_next_step_handler(message, get_location_ru, user_name)


def get_location_uz(message, user_name):
    user_id = message.from_user.id
    if message.location:
        loc = message.location
        db.register_loc(user_id, loc.latitude, loc.longitude)
        bot.send_message(user_id, 'Siz royxatdan otdingiz!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Quyidagi tugma yordamida joylashuvingizni yuboring!')
        bot.register_next_step_handler(message, get_location_uz, user_name)


@bot.message_handler(commands=['weather'])
def forecast(message):
    user_id = message.from_user.id
    name = db.get_username(user_id)
    lat = db.get_loc_lat(user_id)
    lon = db.get_loc_lon(user_id)
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        city = data["name"]
        stat = data["weather"][0]["description"]
        bot.send_message(user_id, f'Привет {name} погода в {city} сейчас: {temp}°C, {stat}')
    else:
        bot.send_message(user_id, 'Что бы воспользоваться функцией, пройдите регистрацию!')


bot.polling()