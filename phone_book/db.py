from config import user, password, host, db_name
import pymysql

from PyQt4 import QtCore
from PyQt4.QtCore import QString

def auth (conn, lgn, psw):

    lgn = str(lgn)
    psw = str(psw)

    sql = "SELECT * FROM users WHERE login=(%s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, lgn)
        result = cursor.fetchone()
        if result:
            if psw == result['password']:
                return True
            else:
                return False
        return False


def register(conn, lgn, psw, birthday):

    lgn = str(lgn)
    psw = str(psw)

    sql = "SELECT * FROM users WHERE login=(%s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, lgn)
        result = cursor.fetchone()
        if result:
            return False

    sql = "INSERT INTO `users` (`login`, `password`, `birthday`) VALUES (%s, %s, %s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, (lgn,psw,birthday))
    conn.commit()
    return True

def add_contact(conn, user, first_name, last_name, phone_number, birthday):
    user=str(user)
    first_name = str(first_name)
    last_name = str(last_name)
    phone_number = str(phone_number)
    sql = "SELECT * FROM contacts WHERE user=(%s) AND first_name=(%s)" \
          "AND last_name=(%s) AND phone_number=(%s) AND birthday=(%s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, (user, first_name, last_name, phone_number, birthday))
        result = cursor.fetchone()
        if result:
            return False

    sql = "INSERT INTO contacts (user, first_name, last_name, phone_number, birthday) " \
          "VALUES (%s, %s, %s, %s, %s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, (user, first_name, last_name, phone_number, birthday))
    conn.commit()
    return True

def get_contacts(conn, username):
    username = str(username)
    sql = "SELECT * FROM contacts WHERE user=(%s) ORDER BY last_name DESC"
    with conn.cursor() as cursor:
        cursor.execute(sql, username)
        result = cursor.fetchall()
        return result

def delete_contact(conn, user, name, phone_number):
    user = str(user)
    (last_name, first_name) = name.split(' ')
    sql = "DELETE FROM contacts WHERE user=(%s) AND first_name=(%s) AND last_name=(%s) AND phone_number=(%s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, (user, first_name, last_name, phone_number))
    conn.commit()

def find_contact(conn, user, name, phone_number):
    user = str(user)
    (last_name, first_name) = name.split(' ')
    sql = "SELECT * FROM contacts WHERE user=(%s) AND first_name=(%s) AND last_name=(%s) AND phone_number=(%s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, (user, first_name, last_name, phone_number))
        result = cursor.fetchone()
        return result

def edit_contact(conn, user, id, first_name, last_name, phone_number, birthday):
    user = str(user)
    first_name = str(first_name)
    last_name = str(last_name)
    sql = "UPDATE contacts SET first_name=(%s),last_name=(%s),phone_number=(%s),birthday=(%s) WHERE id=(%s)"
    with conn.cursor() as cursor:
        cursor.execute(sql, (first_name, last_name, phone_number, birthday, id))
        conn.commit()


def week_birthday(conn, user):
    user = str(user)
    sql = "SELECT * FROM contacts WHERE user=(%s) AND (DAYOFYEAR(birthday)-DAYOFYEAR(CURRENT_DATE())<=7 AND DAYOFYEAR(birthday)>=DAYOFYEAR(CURRENT_DATE())) OR (DAYOFYEAR(CURRENT_DATE())+365-DAYOFYEAR(birthday)<=7 AND DAYOFYEAR(CURRENT_DATE())>DAYOFYEAR(birthday))"
    with conn.cursor() as cursor:
        cursor.execute(sql, user)
        result = cursor.fetchall()
        return result