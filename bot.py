import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from utils_1 import get_random_id
from db.get_user_stats import GetUserStats


vk_session = vk_api.VkApi(token="595e475d34888194a88bdb3039e28a15dafad2248e7e19e4605869e5d5ecbc44d6c142427c0ca9f5321e1")
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            response = event.text.lower()
            user_data = GetUserStats(event.user_id)
            if event.from_user and not event.from_me:
                if response == "начать":
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message="Напиши мне !помощь, что бы посмотреть все мои команды")
                elif response == "!помощь":
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                     message="Вот список моих команд:\n!профиль - для просмотра профиля\n!баланс - просмотр баланса\n!рулетка сумма - сыграть в казино\n!перевод id сумма - перевести деньги пользователю\n!правила - для просмотра правил игры рулетка\n!топ - топ богачей")
                elif response == "!баланс":
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=f"💰Твой баланс: {user_data['money']}")
                elif response == "!профиль":
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=f"🖥Твой ID: {user_data['id']}\n💰Твой баланс: {user_data['money']}\n💻Твой user_id: {user_data['uid']}")
                elif response.split()[0] == "!рулетка":
                    data = roulete_game(event.user_id, int(response.split()[1]))
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=data)
                elif response.split()[0] == "!перевод":
                    try:
                        connect = connection.getConnect()
                        try:
                            with connect.cursor() as cursor:
                                result = cursor.execute(f"SELECT * FROM accounts WHERE id = {response.split()[1]}")
                                row = cursor.fetchone()
                                if int(response.split()[1]) == int(user_data['id']):
                                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                                     message="Вы не можете отправить деньги самому себе")
                                else:
                                    if result == 1:
                                        if int(user_data['money']) < int(response.split()[2]) or int(user_data['money']) < 1:
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
                                                             message=f"Вам пришло {response.split()[2]} от {user_data['uid']}")
                                    else:
                                        vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                                         message="Такого пользователя нет")
                        finally:
                            connect.close()
                    except:
                        vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                         message="Ты не ввел сумму после !перевод")
                elif response == "!правила":
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message="Правила очень простые\nЕсли тебе выпадает число больше 50, то ты выйграл, иначе, увы, проиграл")
                elif response.split()[0] == "/add":
                    data = admin_add_money(event.user_id, int(response.split()[1]), response.split()[2])
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=data)
                elif response.split()[0] == "/nail":
                    data = admin_nail_money(event.user_id, int(response.split()[1]), response.split()[2])
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=data)
                elif response.split()[0] == "/stat":
                    data = admin_seen_stat(event.user_id, response.split()[1])
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=data)
                elif response == "!топ":
                    #data = top_players()
                    #vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=data)
                    connect = connection.getConnect()
                    try:
                        with connect.cursor() as cursor:
                            cursor.execute("SELECT * FROM accounts ORDER BY money DESC")
                            row = cursor.fetchall()
                            for i in row:
                                vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=f"user_id: {i['uid']} Денег: {i['money']}")
                    finally:
                        connect.close()

                elif response.split()[0] == "/chance":
                    data = chance_win(event.user_id, int(response.split()[1]), float(response.split()[2]))
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=data)
                else:
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message="Я тебя не понял, напиши !помощь для просмотра команд")
