from db import pool
import ydb


def update_user_stats(user_id, correct):
    
    def update_stats(session):
        result_set = session.transaction().execute(
            f"SELECT * FROM user_stats WHERE user_id = {user_id};",
            commit_tx=True
        )

        if result_set[0].rows:
            stats = result_set[0].rows[0]
            correct_answers = stats.correct_answers + (1 if correct else 0)
            total_questions = stats.total_questions + 1

            session.transaction().execute(
                f"UPDATE user_stats SET correct_answers = {correct_answers}, total_questions = {total_questions} WHERE user_id = {user_id};",
                commit_tx=True
            )
        else:
            add_answers = 1 if correct else 0
            add_questions = 1

            session.transaction().execute(
                f"INSERT INTO user_stats (user_id, correct_answers, total_questions) VALUES ({user_id}, {add_answers}, {add_questions});",
                commit_tx=True
            )

    pool.retry_operation_sync(update_stats)

def get_user_stats(user_id):

    def select_stats(session):
        result_set = session.transaction(ydb.SerializableReadWrite()).execute(
            f'SELECT correct_answers, total_questions FROM user_stats WHERE user_id = {user_id};',
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_stats)
    if result[0].rows:
        stats = result[0].rows[0]
        return stats.correct_answers, stats.total_questions
    return None