from db.connect_db import get_connect


def check(user_id):
    connection = get_connect()
    try:
        with connection.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM accounts WHERE uid={user_id} AND admin=1")
            if result == 0:
                return False
            else:
                return True
    finally:
        connection.close()
