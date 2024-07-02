from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


markup = ReplyKeyboardBuilder()
quiz_button = KeyboardButton(text='Start Quiz')
stats_button = KeyboardButton(text='Statistics')
markup.add(quiz_button, stats_button)
markup = markup.as_markup(resize_keyboard=True)
