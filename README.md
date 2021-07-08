# phone_book

Инструкция по установке
-----------------------
1. Установить библиотеки `PyQt4`, `pymysql`
2. Установить в файле `config.py` логин и пароль от БД MariaDB
3. Создать базу данных MariaDB с названием **"test_database"**
Перед этим установить кодировку utf8 для базы данных:

        SET character_set_server = 'utf8';
        SET collation_server = 'utf8_unicode_ci';
    
3. Запустить `db_init.py` для создания таблиц в базе данных
4. Запустить `app.py`
