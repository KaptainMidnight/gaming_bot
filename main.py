# -*- charset: utf-8 -*-

from db.get_user_stats import GetUserStats
from vk_api.longpoll import VkEventType, VkLongPoll
import vk_api
from utils_1 import get_random_id
from db.roulette_game import roulete_game
from db.connect_db import get_connect
from db.add_money import addMoney
from db.check_admin import check
from db.nail_money import admin_nail_money
from db.admin_add_money import admin_add_money
from db.admin_change_chance import chance_win
from db.ban_user import ban_users
from db.check_ban import check_ban
from db.unban_user import unban


vk_session = vk_api.VkApi(token="595e475d34888194a88bdb3039e28a15dafad2248e7e19e4605869e5d5ecbc44d6c142427c0ca9f5321e1")
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_username(user_id):
    pass


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            response = event.text.lower()
            if event.from_user and not event.from_me:
                if response == "начать":
                    GetUserStats(event.user_id)
                    vk.messages.send(user_id=event.user_id, message="Напиши мне !помощь для просмотра команд или если Вы жюри, то напишите администратору vk.com/ed100, и сообщите ему этот код PRE-CTSR5-POST",
                                     random_id=get_random_id())
                elif response == "!помощь":
                    if check_ban(event.user_id):
                        vk.messages.send(user_id=event.user_id, message="Вот мой список команд:\n"  # Готово
                                                                        "!профиль - просмотр профиля\n"  # Готово
                                                                        "!рулетка [сумма] - сыграть в рулетку\n"  # Готово
                                                                        "!баланс - просмотр баланса\n"  # Готово
                                                                        "!перевод [id] [сумма] - перевод денег другому игроку\n"  # Готово
                                                                        "!админка - зайти в админ панель",
                                         random_id=get_random_id())
                    else:
                        vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                         random_id=get_random_id())
                elif response == "!профиль":

                    if check_ban(event.user_id):
                        data = GetUserStats(event.user_id)
                        vk.messages.send(user_id=event.user_id, message=
                        f"🖥Твой ID: {data['id']}\n"
                        f"💰Баланс: {data['money']}\n"
                        f"👨‍💻Администратор: {data['admin']}\n"
                        f"🔒Блокировка: {data['ban']}",
                                         random_id=get_random_id())
                    else:
                        vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                         random_id=get_random_id())
                elif response == "!баланс":
                    try:
                        if check_ban(event.user_id):
                            data = GetUserStats(event.user_id)
                            vk.messages.send(user_id=event.user_id, message=f"💰Баланс: {data['money']}",
                                             random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                             random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message='Что-то пошло не так',
                                         random_id=get_random_id())
                elif response.split()[0] == "!рулетка":
                    try:
                        if check_ban(event.user_id):
                            vk.messages.send(user_id=event.user_id,
                                             message=roulete_game(event.user_id, int(response.split()[1])),
                                             random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                             random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так",
                                         random_id=get_random_id())
                elif response.split()[0] == "!перевод":
                    try:
                        data = GetUserStats(event.user_id)
                        connect = get_connect()
                        if check_ban(event.user_id):
                            try:
                                with connect.cursor() as cursor:
                                    result = cursor.execute(f"SELECT * FROM accounts WHERE id = {response.split()[1]}")
                                    row = cursor.fetchone()
                                    if int(response.split()[1]) == int(data['id']):
                                        vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                                         message="Вы не можете отправить деньги самому себе")
                                    else:
                                        if result == 1:
                                            if int(data['money']) < int(response.split()[2]) or int(data['money']) < 1:
                                                vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                                                 message="У тебя не достаточно денег")
                                            addMoney(event.user_id, int(response.split()[2]), 2)
                                            addMoney(int(row['uid']), int(response.split()[2]), 1)
                                            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                                             message=f"Вы отправили деньги пользователю: {response.split()[1]}")
                                            user_friend = cursor.execute(
                                                f"SELECT * FROM accounts WHERE id = {response.split()[1]}")
                                            user = cursor.fetchone()
                                            if user_friend == 1:
                                                vk.messages.send(user_id=int(user['uid']), random_id=get_random_id(),
                                                                 message=f"Вам пришло {response.split()[2]} от {data['uid']}")
                                        else:
                                            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                                             message="Такого пользователя нет")
                            finally:
                                connect.close()
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                             random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так",
                                         random_id=get_random_id())
                elif response.split()[0] == "!админка":
                    if check_ban(event.user_id):
                        if not check(event.user_id):
                            vk.messages.send(user_id=event.user_id, message="Access denied", random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вот твой список команд:\n"
                                                                            "/nail [id] [сумма] - забрать деньги у пользователя\n"
                                                                            "/add [id] [сумма] - добавить игроку деньги\n"
                                                                            "/chance [id] [шанс] - установить игроку шанс выигрыша\n"
                                                                            "/ban [id] - забанить игрока\n"
                                                                            "/unban [id] -  разблокировать пользователя", random_id=get_random_id())
                    else:
                        vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                         random_id=get_random_id())
                elif response.split()[0] == "/nail":
                    try:
                        if check_ban(event.user_id):
                            if not check(event.user_id):
                                vk.messages.send(user_id=event.user_id, message="Access denied", random_id=get_random_id())
                            else:
                                vk.messages.send(user_id=event.user_id, message=admin_nail_money(event.user_id, int(response.split()[1]), int(response.split()[2])), random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                             random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так", random_id=get_random_id())
                elif response.split()[0] == "/add":
                    try:
                        if check_ban(event.user_id):
                            if not check(event.user_id):
                                vk.messages.send(user_id=event.user_id, message="Access denied", random_id=get_random_id())
                            else:
                                vk.messages.send(user_id=event.user_id, message=admin_add_money(event.user_id, int(response.split()[1]), int(response.split()[2])), random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                             random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так", random_id=get_random_id())
                elif response.split()[0] == "/chance":
                    try:
                        if check_ban(event.user_id):
                            if not check(event.user_id):
                                vk.messages.send(user_id=event.user_id, message="Access denied", random_id=get_random_id())
                            else:
                                vk.messages.send(user_id=event.user_id, message=chance_win(event.user_id, int(response.split()[1]), int(response.split()[2])), random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны",
                                             random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так",
                                         random_id=get_random_id())
                elif response.split()[0] == "/ban":
                    try:
                        if check_ban(event.user_id):
                            if not check(event.user_id):
                                vk.messages.send(user_id=event.user_id, message="Access denied", random_id=get_random_id())
                            else:
                                vk.messages.send(user_id=event.user_id, message=ban_users(event.user_id, int(response.split()[1])), random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны", random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так",
                                         random_id=get_random_id())
                elif response.split()[0] == "/unban":
                    try:
                        if check_ban(event.user_id):
                            if not check(event.user_id):
                                vk.messages.send(user_id=event.user_id, message="Access denied", random_id=get_random_id())
                            else:
                                vk.messages.send(user_id=event.user_id, message=unban(int(response.split()[1])), random_id=get_random_id())
                        else:
                            vk.messages.send(user_id=event.user_id, message="Вы забокированны", random_id=get_random_id())
                    except:
                        vk.messages.send(user_id=event.user_id, message="Что-то пошло не так",
                                         random_id=get_random_id())
                else:
                    vk.messages.send(user_id=event.user_id,
                                     message="Я тебя не понял, напиши мне !помощь для просмотра команд",
                                     random_id=get_random_id())
