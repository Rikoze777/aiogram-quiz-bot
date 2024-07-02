import sqlite3
from questions import questions


def initialize_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats (
                        user_id INTEGER NOT NULL,
                        correct_answers INTEGER NOT NULL,
                        total_questions INTEGER NOT NULL,
                        PRIMARY KEY (user_id))''')

    cursor.executemany('INSERT INTO questions (question, answer) VALUES (?, ?)', questions)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()