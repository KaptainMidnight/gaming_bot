from db.connect_db import get_connect
from db.add_money import addMoney


def admin_nail_money(my_user_id, id, money):
    connect = get_connect()  # Подключаемся к БД
    try:
        with connect.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM accounts WHERE uid={my_user_id}")
            if result == 1:
                result = cursor.execute(f"SELECT * FROM accounts WHERE id={id}")
                row = cursor.fetchone()
                if result == 1:
                    addMoney(row['uid'], int(money), 2)
                    return "Деньги забранны"
    finally:
        connect.close()
