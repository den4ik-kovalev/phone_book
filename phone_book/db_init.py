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

sql = 'CREATE TABLE `users` (' \
      '`login` varchar(255) NOT NULL,' \
      '`password` varchar(255) NOT NULL,' \
      '`birthday` date NOT NULL,' \
      'PRIMARY KEY (`login`)' \
      ')'


with connection.cursor() as cursor:
    cursor.execute(sql)
connection.commit()

with connection.cursor() as cursor:
    sql = "INSERT INTO `users` (`login`, `password`, `birthday`) VALUES (%s, %s, %s)"
    cursor.execute(sql, ('admin', 'password', '2000-01-01'))
connection.commit()

sql = 'CREATE TABLE `contacts` (' \
      '`id` int NOT NULL AUTO_INCREMENT,' \
      '`user` varchar(255) NOT NULL,' \
      '`first_name` varchar(255) NOT NULL,' \
      '`last_name` varchar(255) NOT NULL,' \
      '`phone_number` varchar(255) NOT NULL,' \
      '`birthday` date NOT NULL,' \
      'PRIMARY KEY (`id`)' \
      ')'


with connection.cursor() as cursor:
    cursor.execute(sql)
connection.commit()



