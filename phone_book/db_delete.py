from config import user, password, host, db_name
import pymysql

connection = pymysql.connect(
    user=user,
    password=password,
    host=host,
    port=3306,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)

sql = 'DROP TABLE `users`'


with connection.cursor() as cursor:
    cursor.execute(sql)
connection.commit()

sql = 'DROP TABLE `contacts`'


with connection.cursor() as cursor:
    cursor.execute(sql)
connection.commit()