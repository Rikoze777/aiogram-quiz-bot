import sqlite3


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
