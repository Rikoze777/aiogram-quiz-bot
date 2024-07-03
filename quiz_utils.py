import sqlite3
from aiogram.filters.state import State, StatesGroup


class QuizStates(StatesGroup):
    awaiting_answer = State()


def get_question():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, question FROM questions ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()
    conn.close()
    return question

def check_answer(question_id, answer):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT answer FROM questions WHERE id = ?', (question_id,))
    correct_answer = cursor.fetchone()[0]
    conn.close()
    return correct_answer.lower() == answer.lower()
