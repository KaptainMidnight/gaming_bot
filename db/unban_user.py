from db.connect_db import get_connect


def unban(id):
    connection = get_connect()
    try:
        with connection.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM accounts WHERE id={id} AND ban=1")
            if result == 1:
                cursor.execute(f"UPDATE accounts SET ban=0 WHERE id={id}")
                connection.commit()
                return "Пользователь разблокирован"
            else:
                return "Пользователя не существует, либо он не заблокирован"
    finally:
        connection.close()
