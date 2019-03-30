from db.connect_db import get_connect
from db.add_money import addMoney
from db.get_user_stats import GetUserStats
from random import random


def roulete_game(my_user_id, money):
    connect = get_connect()
    try:
        with connect.cursor() as cursor:
            user_data = GetUserStats(my_user_id)
            if int(user_data['money']) < money or int(user_data['money']) <= 0:
                return "У тебя не хватает денег на игру"
            else:
                cursor.execute(f"SELECT * FROM accounts WHERE uid={my_user_id}")
                row = cursor.fetchone()
                if random() > float(row['chance']):
                    addMoney(my_user_id, money, 2)
                    return f"Прости, но ты проиграл: {money}"
                else:
                    addMoney(my_user_id, money, 1)
                    return f"Поздравляю, ты выйграл: {money}"
    finally:
        connect.close()
