import sqlite3
from aiogram.filters.state import State, StatesGroup


class QuizStates(StatesGroup):
    question = State()
    finished = State()


def get_all_questions():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return questions

def check_answer(question_id, selected_option):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT correct_option FROM questions WHERE id = ?', (question_id,))
    correct_option = cursor.fetchone()[0]
    conn.close()
    return int(selected_option.split('_')[1]) == correct_option
