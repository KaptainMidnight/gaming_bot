from db.connect_db import get_connect


def chance_win(my_user_id, id, chance):
    connect = get_connect()
    try:
        with connect.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM accounts WHERE uid={my_user_id}")
            if result == 1:
                result = cursor.execute(f"SELECT * FROM accounts WHERE id={id}")
                if result == 1:
                    cursor.execute(f"UPDATE accounts SET chance={chance} WHERE id={id}")
                    connect.commit()
                else:
                    return "Не верно введен id пользователя"
                return "Изменения скоро вступят в силу"
    finally:
        connect.close()
