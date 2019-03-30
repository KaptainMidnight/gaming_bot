from db.connect_db import get_connect


def ban_users(my_user_id, id):
    connection = get_connect()
    try:
        with connection.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM accounts WHERE id={id} AND ban=0")
            if result == 0:
                return "Такого пользователья нет или он уже заблокирован"
            else:
                cursor.execute(f"UPDATE accounts SET ban=1 WHERE id={id}")
                connection.commit()
                return "Пользователь заблокирован"
    finally:
        connection.close()
