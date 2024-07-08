from aiogram import Router
from aiogram.filters import Command

from quiz_utils import check_answer, get_all_questions
from stats_utils import get_user_stats, update_user_stats
from aiogram import types
from keyboard import markup
from aiogram.fsm.context import FSMContext
from quiz_utils import QuizStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


router = Router()

user_data = {}


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Welcome to the quiz bot! Press 'Start Quiz' to begin.", reply_markup=markup)


@router.callback_query(lambda c: c.data == 'start_quiz')
async def start_quiz(callback_query: types.CallbackQuery, state: FSMContext):
    questions = get_all_questions()
    await state.update_data(questions=questions, current_question=0)

    question_data = questions[0]
    question_id, question_text, options, _ = question_data
    options_list = options.split('|')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=option, callback_data=f"answer_{idx}") for idx, option in enumerate(options_list)]
    ])
    
    user_data[callback_query.from_user.id] = question_id
    await callback_query.message.answer(question_text, reply_markup=keyboard)
    await state.set_state(QuizStates.question)
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


@router.callback_query(lambda c: c.data.startswith('answer'))
async def handle_answer(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    data = await state.get_data()
    questions = data.get('questions')
    current_question = data.get('current_question')

    if user_id in user_data:
        question_id = user_data[user_id]
        selected_option = callback_query.data
        correct = check_answer(question_id, selected_option)
        update_user_stats(user_id, correct)
        if correct:
            await callback_query.message.answer('Correct! 🎉')
        else:
            await callback_query.message.answer('Incorrect. Try again!')
        current_question += 1
        if current_question < len(questions):
            question_data = questions[current_question]
            question_id, question_text, options, _ = question_data
            options_list = options.split('|')

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=option, callback_data=f"answer_{idx}") for idx, option in enumerate(options_list)]
            ])

            user_data[callback_query.from_user.id] = question_id
            await callback_query.message.answer(question_text, reply_markup=keyboard)
            await state.update_data(current_question=current_question)

        else:
            await callback_query.message.answer("Quiz finished!")
            await state.set_state(QuizStates.finished)
        await callback_query.message.edit_reply_markup(reply_markup=None)
    else:
        await callback_query.message.answer("Please start a quiz by selecting 'Start Quiz'.")

