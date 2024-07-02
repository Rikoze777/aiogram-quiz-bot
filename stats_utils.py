import sqlite3


def update_user_stats(user_id, correct):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    stats = cursor.fetchone()
    if stats:
        correct_answers = stats[1] + (1 if correct else 0)
        total_questions = stats[2] + 1
        cursor.execute('UPDATE user_stats SET correct_answers = ?, total_questions = ? WHERE user_id = ?',
                       (correct_answers, total_questions, user_id))
    else:
        cursor.execute('INSERT INTO user_stats (user_id, correct_answers, total_questions) VALUES (?, ?, ?)',
                       (user_id, 1 if correct else 0, 1))
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT correct_answers, total_questions FROM user_stats WHERE user_id = ?', (user_id,))
    stats = cursor.fetchone()
    conn.close()
    return stats
