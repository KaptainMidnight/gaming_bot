import pymysql.cursors


def get_connect():
    connection = pymysql.Connect(
        host="localhost",
        user="root",
        password="root",
        db="vkbot",
        unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
