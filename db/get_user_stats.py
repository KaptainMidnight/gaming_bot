from db.connect_db import get_connect


def GetUserStats(user_id):
    connect = get_connect()
    try:
        while True:
            with connect.cursor() as cursor:
                sql = f"SELECT * FROM accounts WHERE uid = {user_id}"
                result = cursor.execute(sql)  # Count records
                row = cursor.fetchone()  # Take in the dictionary

                if result >= 1:
                    return row
                else:
                    cursor.execute(f"INSERT INTO accounts(uid, money) VALUES({user_id}, 500)")
                    cursor.execute(f"SELECT * FROM accounts WHERE uid = {user_id}")
                    connect.commit()
                    return row

    finally:
        connect.close()
