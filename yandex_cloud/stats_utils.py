
from db import pool

def update_user_stats(user_id, correct):

    def update_stats(session):
        result_set = session.transaction().execute(
            'SELECT * FROM user_stats WHERE user_id = ?',
            (user_id,),
            commit_tx=True
        )

        if result_set[0].rows:
            stats = result_set[0].rows[0]
            correct_answers = stats['correct_answers'] + (1 if correct else 0)
            total_questions = stats['total_questions'] + 1
            session.transaction().execute(
                'UPDATE user_stats SET correct_answers = ?, total_questions = ? WHERE user_id = ?',
                (correct_answers, total_questions, user_id),
                commit_tx=True
            )
        else:
            session.transaction().execute(
                'UPSERT INTO user_stats (user_id, correct_answers, total_questions) VALUES (?, ?, ?)',
                (user_id, 1 if correct else 0, 1),
                commit_tx=True
            )

    pool.retry_operation_sync(update_stats)

def get_user_stats(user_id):

    def select_stats(session):
        result_set = session.transaction().execute(
            'SELECT correct_answers, total_questions FROM user_stats WHERE user_id = ?',
            (user_id,),
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_stats)
    if result[0].rows:
        stats = result[0].rows[0]
        return stats['correct_answers'], stats['total_questions']
    return None