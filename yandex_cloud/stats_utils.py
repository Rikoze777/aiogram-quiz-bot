from db import pool
import ydb


def update_user_stats(user_id, correct):
    
    def update_stats(session):
        params = {
            '$user_id': user_id,
        }
        result_set = session.transaction(ydb.SerializableReadWrite()).execute(
            'DECLARE $user_id AS Uint64; SELECT * FROM user_stats WHERE user_id = $user_id;',
            params,
            commit_tx=True
        )

        if result_set[0].rows:
            stats = result_set[0].rows[0]
            correct_answers = stats.correct_answers + (1 if correct else 0)
            total_questions = stats.total_questions + 1
            ses_params = {
                '$user_id': user_id,
                '$correct_answers': correct_answers,
                '$total_questions': total_questions,
            }
            session.transaction(ydb.SerializableReadWrite()).execute(
                """DECLARE $user_id AS Uint64;
                    DECLARE $correct_answers AS Uint64;
                    DECLARE $total_questions AS Uint64;
                    UPDATE user_stats SET correct_answers = $correct_answers, total_questions = $total_questions WHERE user_id = $user_id;""",
                ses_params,
                commit_tx=True
            )
        else:
            ses_params = {
                    '$user_id': user_id,
                    '$correct_answers': 1 if correct else 0,
                    '$total_questions': 1,
                }
            session.transaction(ydb.SerializableReadWrite()).execute(
                """DECLARE $user_id AS Uint64;
                    DECLARE $correct_answers AS Uint64;
                    DECLARE $total_questions AS Uint64;
                    UPSERT INTO user_stats (user_id, correct_answers, total_questions) VALUES ($user_id, $correct_answers, $total_questions);""",
                ses_params,
                correct_answers=1 if correct else 0,
                total_questions=1,
                commit_tx=True
            )

    pool.retry_operation_sync(update_stats)

def get_user_stats(user_id):

    def select_stats(session):
        ses_params = {
                    '$user_id': user_id,
                } 
        result_set = session.transaction(ydb.SerializableReadWrite()).execute(
            'DECLARE $user_id AS Uint64; SELECT correct_answers, total_questions FROM user_stats WHERE user_id = $user_id;',
            ses_params,
            commit_tx=True
        )
        return result_set

    result = pool.retry_operation_sync(select_stats)
    if result[0].rows:
        stats = result[0].rows[0]
        return stats.correct_answers, stats.total_questions
    return None
