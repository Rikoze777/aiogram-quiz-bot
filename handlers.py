from aiogram import Router
from aiogram.filters import Command

from quiz_utils import check_answer, get_question
from stats_utils import get_user_stats, update_user_stats
from aiogram import types
from keyboard import markup
from aiogram.fsm.context import FSMContext
from quiz_utils import QuizStates


router = Router()

user_data = {}


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Welcome to the quiz bot! Press 'Start Quiz' to begin.", reply_markup=markup)


@router.callback_query(lambda c: c.data == 'start_quiz')
async def start_quiz(callback_query: types.CallbackQuery, state: FSMContext):
    question = get_question()
    user_data[callback_query.from_user.id] = question[0]
    await callback_query.message.answer(question[1])
    await state.set_state(QuizStates.awaiting_answer)
    await callback_query.message.edit_reply_markup(reply_markup=None)


@router.callback_query(lambda c: c.data == 'statistics')
async def show_statistics(callback_query: types.CallbackQuery):
    stats = get_user_stats(callback_query.from_user.id)
    if stats:
        correct_answers, total_questions = stats
        await callback_query.message.answer(f'You have answered {correct_answers} out of {total_questions} questions correctly.', reply_markup=markup)
    else:
        await callback_query.message.answer('You have not participated in the quiz yet.', reply_markup=markup)
    await callback_query.message.edit_reply_markup(reply_markup=None)


@router.message(QuizStates.awaiting_answer)
async def handle_answer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in user_data:
        question_id = user_data[user_id]
        answer = message.text
        correct = check_answer(question_id, answer)
        update_user_stats(user_id, correct)
        if correct:
            await message.answer('Correct! 🎉', reply_markup=markup)
        else:
            await message.answer('Incorrect. Try again!', reply_markup=markup)
        del user_data[user_id]
        await state.clear()
    else:
        await message.answer("Please start a quiz by selecting 'Start Quiz'.")