from aiogram import Router
from aiogram.filters import Command

from quiz_utils import check_answer, get_question
from stats_utils import get_user_stats, update_user_stats
from aiogram import types
from keyboard import markup


router = Router()

user_data = {}


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Welcome to the quiz bot! Press 'Start Quiz' to begin.", reply_markup=markup)


@router.message(lambda message: message.text == 'Start Quiz')
async def start_quiz(message: types.Message):
    question = get_question()
    user_data[message.from_user.id] = question[0]
    await message.answer(question[1])


@router.message(lambda message: message.text == 'Statistics')
async def show_statistics(message: types.Message):
    stats = get_user_stats(message.from_user.id)
    if stats:
        correct_answers, total_questions = stats
        await message.answer(f'You have answered {correct_answers} out of {total_questions} questions correctly.')
    else:
        await message.answer('You have not participated in the quiz yet.')


@router.message()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_data:
        question_id = user_data[user_id]
        correct = check_answer(question_id, message.text)
        update_user_stats(user_id, correct)
        if correct:
            await message.answer('Correct! 🎉', reply_markup=markup)
        else:
            await message.answer('Incorrect. Try again!', reply_markup=markup)
        del user_data[user_id]
    else:
        await message.answer("Please start a quiz by pressing 'Start Quiz'.")
