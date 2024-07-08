from aiogram.filters.state import State, StatesGroup
from db import pool
import ydb


class QuizStates(StatesGroup):
    question = State()
    finished = State()


def get_all_questions():
    def select_questions(session):
        result_set = session.transaction(ydb.SerializableReadWrite()).execute(
            'SELECT id, question, options, correct_option FROM questions;',
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_questions)
    questions = []
    for row in result[0].rows:
        question = {
            'id': row.id,
            'question': row.question,
            'options': row.options.split('|'),
            'correct_option': row.correct_option
        }
        questions.append(question)
    return questions


def check_answer(question_id, selected_option):
    params = {
            '$id': question_id,
        }
    def select_correct_option(session):
        result_set = session.transaction(ydb.SerializableReadWrite()).execute(
            'DECLARE $id AS Uint64; SELECT correct_option FROM questions WHERE id = $id;',
            params,
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_correct_option)
    correct_option = result[0].rows[0].correct_option
    print('corr_opt', int(correct_option))
    print('check', int(selected_option.split('_')[1]))
    return int(selected_option.split('_')[1]) == int(correct_option)

