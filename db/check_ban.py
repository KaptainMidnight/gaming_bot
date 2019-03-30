from db.connect_db import get_connect
from db.get_user_stats import GetUserStats


def check_ban(user_id):
    connection = get_connect()
    try:
        with connection.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM accounts WHERE uid={user_id} AND ban=1")
            row = cursor.fetchone()
            if result == 1:
                return False
            else:
                return True
    finally:
        connection.close()
