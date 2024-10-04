from telebot import types


def choose_lang():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('RU')
    but2 = types.KeyboardButton('UZ')
    kb.add(but1, but2)

    return kb


def cont_ru():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Продолжить')
    kb.add(but)

    return kb


def cont_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = types.KeyboardButton('Davom etish')
    kb.add(but)

    return kb


def number_button_ru():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(but1)

    return kb


def number_button_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Raqam yuboring', request_contact=True)
    kb.add(but1)

    return kb


def location_button_ru():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(but1)

    return kb


def location_button_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Joylashuvni yuborish', request_location=True)
    kb.add(but1)

    return kb