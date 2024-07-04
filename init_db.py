import sqlite3
from questions import quiz_data

def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    # Создание таблицы вопросов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_option INTEGER NOT NULL
    )
    ''')

    # Создание таблицы статистики пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        user_id INTEGER PRIMARY KEY,
        correct_answers INTEGER NOT NULL,
        total_questions INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def insert_questions(data):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    for question in data:
        options = '|'.join(question['options'])
        cursor.execute('''
        INSERT INTO questions (question, options, correct_option)
        VALUES (?, ?, ?)
        ''', (question['question'], options, question['correct_option']))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_questions(quiz_data)