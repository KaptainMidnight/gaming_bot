from db.connect_db import get_connect


def addMoney(user_id, money, status):
    connect = get_connect()
    try:
        with connect.cursor() as cursor:
            result = cursor.execute(f"SELECT * FROM `accounts` WHERE `uid` = {user_id}")
            row = cursor.fetchone()
            if status == 1 and result == 1:
                row['money'] += money
            elif status == 2 and result >= 1:
                row['money'] -= money
            cursor.execute(f"UPDATE accounts SET money= {row['money']} WHERE uid = {user_id}")
            connect.commit()
    except:
        connect.close()
