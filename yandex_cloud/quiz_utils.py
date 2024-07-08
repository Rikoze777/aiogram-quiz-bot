from aiogram.filters.state import State, StatesGroup
from db import pool


class QuizStates(StatesGroup):
    question = State()
    finished = State()


def get_all_questions():
    def select_questions(session):
        result_set = session.transaction().execute(
            'SELECT * FROM questions',
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_questions)
    questions = []
    for row in result[0].rows:
        question = {
            'id': row['id'],
            'question': row['question'],
            'options': row['options'].split('|'),
            'correct_option': row['correct_option']
        }
        questions.append(question)
    return questions

def check_answer(question_id, selected_option):

    def select_correct_option(session):
        result_set = session.transaction().execute(
            'SELECT correct_option FROM questions WHERE id = ?',
            (question_id,),
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_correct_option)
    correct_option = result[0].rows[0]['correct_option']
    return int(selected_option.split('_')[1]) == correct_option
