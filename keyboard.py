from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


markup = InlineKeyboardBuilder()
quiz_button = InlineKeyboardButton(text='Start Quiz', callback_data='start_quiz')
stats_button = InlineKeyboardButton(text='Statistics', callback_data='statistics')
markup.add(quiz_button, stats_button)
markup = markup.as_markup(resize_keyboard=True)
