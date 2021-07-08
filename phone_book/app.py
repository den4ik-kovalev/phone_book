# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QPushButton, QDialog, QMessageBox, QTableWidgetItem, QListWidgetItem
from PyQt4.QtCore import QString, QSettings

from config import user, password, host, db_name
import pymysql
import db

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

connection = pymysql.connect(
        user=user,
        password=password,
        host=host,
        port=3306,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )


class Auth(QMainWindow):
    def __init__(self):
        super(Auth, self).__init__()
        uic.loadUi('UI/auth.ui', self)
        self.pushButton.clicked.connect(self.loginfunction)
        self.pushButton_2.clicked.connect(self.show_register_window)
        self.pushButton_3.clicked.connect(self.close)
        self.checkBox_2.stateChanged.connect(self.show_password)
        self.checkBox.stateChanged.connect(self.remember_me)
        self.label_2.mousePressEvent = self.show_password_window
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit.clearFocus()

    def show_register_window(self):
        self.register_window = Register()
        self.register_window.show()

    def show_password_window(self, event):
        self.password_window = ForgetPassword()
        self.password_window.show()

    def show_phonebook_window(self, username):
        self.phonebook_window = PhoneBook(username)
        self.phonebook_window.show()
        self.close()

    def loginfunction(self):
        global connection
        lgn = self.lineEdit.text().toUtf8()
        psw = self.lineEdit_2.text().toUtf8()

        if not db.auth(connection,lgn,psw):
            error = QMessageBox()
            error.setWindowTitle(u'Ошибка')
            error.setText(u'Неверная пара логин-пароль')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            global SETTINGS
            lgn = str(lgn)
            if SETTINGS.value('remember_me') != False:
                SETTINGS.setValue('user', lgn)
            self.show_phonebook_window(lgn)

    def show_password(self, state):
        if state == QtCore.Qt.Checked:
            self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)

    def remember_me(self, state):
        global SETTINGS
        if state == QtCore.Qt.Checked:
            SETTINGS.setValue('remember_me', True)
        else:
            SETTINGS.setValue('remember_me', False)




class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        uic.loadUi('UI/register.ui', self)
        self.pushButton.clicked.connect(self.registerfunction)
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QtGui.QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.close)

    def registerfunction(self):
        global connection
        lgn = self.lineEdit.text().toUtf8()
        psw = self.lineEdit_2.text().toUtf8()
        psw2 = self.lineEdit_3.text().toUtf8()

        birthday = str(self.dateEdit.dateTime().toString('yyyy-MM-dd'))

        if not (lgn and psw and psw2):
            error = QMessageBox()
            error.setWindowTitle(u'Ошибка')
            error.setText(u'Все поля должны быть заполнены')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            if psw != psw2:
                error = QMessageBox()
                error.setWindowTitle(u'Ошибка')
                error.setText(u'Пароли не совпадают')
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
            else:
                if not db.register(connection,lgn,psw, birthday):
                    error = QMessageBox()
                    error.setWindowTitle(u'Ошибка')
                    error.setText(u'Этот логин уже зарегистрирован')
                    error.setIcon(QMessageBox.Warning)
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()
                else:
                    success = QMessageBox()
                    success.setWindowTitle(u'Успех')
                    success.setText(u'Вы успешно зарегистрированы')
                    success.setIcon(QMessageBox.Information)
                    success.setStandardButtons(QMessageBox.Ok)
                    success.exec_()
                    self.close()


class ForgetPassword(QMainWindow):
    def __init__(self):
        super(ForgetPassword, self).__init__()
        uic.loadUi('UI/password.ui', self)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.close)


class PhoneBook(QMainWindow):
    def __init__(self, login):
        super(PhoneBook, self).__init__()
        uic.loadUi('UI/phonebook.ui', self)
        self.username = login
        self.label_2.setText(_translate("MainWindow", self.username, None))
        self.pushButton.clicked.connect(self.add_contact)
        self.pushButton_2.clicked.connect(self.edit_contact)
        self.pushButton_3.clicked.connect(self.delete_contact)
        self.pushButton_4.clicked.connect(self.show_table)
        self.pushButton_5.clicked.connect(self.exit)
        self.show()
        self.show_table()
        self.show_birthdays()

    def show_birthdays(self):
        global connection
        birthdays = db.week_birthday(connection, self.username)
        if birthdays:
            success = QMessageBox()
            success.setWindowTitle(u'Дни рождения')
            items = _translate("MainWindow", 'Дни рождения на ближайшую неделю: \n', None)
            for contact in birthdays:
                items += _translate("MainWindow", contact['last_name'], None)+' '+_translate("MainWindow", contact['first_name'], None)+': '+str(contact['birthday'])+'\n'
            success.setText(items)
            success.setIcon(QMessageBox.Information)
            success.setStandardButtons(QMessageBox.Ok)
            success.exec_()
        else:
            success = QMessageBox()
            success.setWindowTitle(u'Дни рождения')
            success.setText(u'Нет дней рождения на этой неделе')
            success.setIcon(QMessageBox.Information)
            success.setStandardButtons(QMessageBox.Ok)
            success.exec_()

    def exit(self):
        global SETTINGS
        SETTINGS.setValue('remember_me', False)
        SETTINGS.setValue('user', None)
        self.auth_window = Auth()
        self.auth_window.show()
        self.close()

    def add_contact(self):
        self.add_contact_window = AddContact(self.username)
        self.add_contact_window.show()

    def delete_contact(self):
        self.delete_contact_window = DeleteContact(self.username)
        self.delete_contact_window.show()

    def edit_contact(self):
        self.edit_contact_window = EditContact(self.username)
        self.edit_contact_window.show()

    def get_contacts(self, username):
        global connection
        return db.get_contacts(connection, username)

    def show_table(self):
        contacts = self.get_contacts(self.username)

        self.tableWidget.setRowCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_8.setRowCount(0)
        self.tableWidget_9.setRowCount(0)
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_12.setRowCount(0)
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_14.setRowCount(0)

        for row_data in contacts:
            name = row_data['last_name'] +' '+row_data['first_name']
            phone_number = row_data['phone_number']
            birthday = row_data['birthday']

            i1 = i2 = i3 = i4 = i5 = i6 = i7 = i8 = i9 = i10 = i11 = i12 = i13 = i14 = 0
            letter = name[:2]
            if (letter == 'А') or (letter == 'а') or (letter == 'Б') or (letter == 'б'):
                self.tableWidget.insertRow(i1)
                self.tableWidget.setItem(i1, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget.setItem(i1, 1, QTableWidgetItem(phone_number))
                self.tableWidget.setItem(i1, 2, QTableWidgetItem(str(birthday)))
                i1 += 1
            elif (letter == 'В') or (letter == 'в') or (letter == 'Г') or (letter == 'г'):
                self.tableWidget_2.insertRow(i2)
                self.tableWidget_2.setItem(i2, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_2.setItem(i2, 1, QTableWidgetItem(phone_number))
                self.tableWidget_2.setItem(i2, 2, QTableWidgetItem(str(birthday)))
                i2 += 1
            elif (letter == 'Д') or (letter == 'д') or (letter == 'Е') or (letter == 'е'):
                self.tableWidget_3.insertRow(i3)
                self.tableWidget_3.setItem(i3, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_3.setItem(i3, 1, QTableWidgetItem(phone_number))
                self.tableWidget_3.setItem(i3, 2, QTableWidgetItem(str(birthday)))
                i3 += 1
            elif (letter == 'Ж') or (letter == 'ж') or (letter == 'З') or (letter == 'з') or (letter == 'И') or (letter == 'и') or (letter == 'Й') or (letter == 'й'):
                self.tableWidget_4.insertRow(i4)
                self.tableWidget_4.setItem(i4, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_4.setItem(i4, 1, QTableWidgetItem(phone_number))
                self.tableWidget_4.setItem(i4, 2, QTableWidgetItem(str(birthday)))
                i4 += 1
            elif (letter == 'К') or (letter == 'к') or (letter == 'Л') or (letter == 'л'):
                self.tableWidget_5.insertRow(i5)
                self.tableWidget_5.setItem(i5, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_5.setItem(i5, 1, QTableWidgetItem(phone_number))
                self.tableWidget_5.setItem(i5, 2, QTableWidgetItem(str(birthday)))
                i5 += 1
            elif (letter == 'М') or (letter == 'м') or (letter == 'Н') or (letter == 'н'):
                self.tableWidget_6.insertRow(i6)
                self.tableWidget_6.setItem(i6, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_6.setItem(i6, 1, QTableWidgetItem(phone_number))
                self.tableWidget_6.setItem(i6, 2, QTableWidgetItem(str(birthday)))
                i6 += 1
            elif (letter == 'О') or (letter == 'о') or (letter == 'П') or (letter == 'п'):
                self.tableWidget_7.insertRow(i7)
                self.tableWidget_7.setItem(i7, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_7.setItem(i7, 1, QTableWidgetItem(phone_number))
                self.tableWidget_7.setItem(i7, 2, QTableWidgetItem(str(birthday)))
                i7 += 1
            elif (letter == 'Р') or (letter == 'р') or (letter == 'С') or (letter == 'с'):
                self.tableWidget_8.insertRow(i8)
                self.tableWidget_8.setItem(i8, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_8.setItem(i8, 1, QTableWidgetItem(phone_number))
                self.tableWidget_8.setItem(i8, 2, QTableWidgetItem(str(birthday)))
                i8 += 1
            elif (letter == 'Т') or (letter == 'т') or (letter == 'У') or (letter == 'у'):
                self.tableWidget_13.insertRow(i9)
                self.tableWidget_13.setItem(i9, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_13.setItem(i9, 1, QTableWidgetItem(phone_number))
                self.tableWidget_13.setItem(i9, 2, QTableWidgetItem(str(birthday)))
                i9 += 1
            elif (letter == 'Ф') or (letter == 'ф') or (letter == 'Х') or (letter == 'х'):
                self.tableWidget_9.insertRow(i10)
                self.tableWidget_9.setItem(i10, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_9.setItem(i10, 1, QTableWidgetItem(phone_number))
                self.tableWidget_9.setItem(i10, 2, QTableWidgetItem(str(birthday)))
                i10 += 1
            elif (letter == 'Ц') or (letter == 'ц') or (letter == 'Ч') or (letter == 'ч') or (letter == 'Ш') or (letter == 'ш') or (letter == 'Щ') or (letter == 'щ'):
                self.tableWidget_10.insertRow(i11)
                self.tableWidget_10.setItem(i11, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_10.setItem(i11, 1, QTableWidgetItem(phone_number))
                self.tableWidget_10.setItem(i11, 2, QTableWidgetItem(str(birthday)))
                i11 += 1
            elif (letter == 'Ъ') or (letter == 'ъ') or (letter == 'Ы') or (letter == 'ы') or (letter == 'Ь') or (letter == 'ь'):
                self.tableWidget_11.insertRow(i12)
                self.tableWidget_11.setItem(i12, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_11.setItem(i12, 1, QTableWidgetItem(phone_number))
                self.tableWidget_11.setItem(i12, 2, QTableWidgetItem(str(birthday)))
                i12 += 1
            elif (letter == 'Э') or (letter == 'э') or (letter == 'Ю') or (letter == 'ю') or (letter == 'Я') or (letter == 'я'):
                self.tableWidget_12.insertRow(i13)
                self.tableWidget_12.setItem(i13, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_12.setItem(i13, 1, QTableWidgetItem(phone_number))
                self.tableWidget_12.setItem(i13, 2, QTableWidgetItem(str(birthday)))
                i13 += 1
            else:
                self.tableWidget_14.insertRow(i14)
                self.tableWidget_14.setItem(i14, 0, QTableWidgetItem(_translate("MainWindow", name, None)))
                self.tableWidget_14.setItem(i14, 1, QTableWidgetItem(phone_number))
                self.tableWidget_14.setItem(i14, 2, QTableWidgetItem(str(birthday)))
                i14 += 1


class AddContact(QWidget):
    def __init__(self, login):
        super(AddContact, self).__init__()
        uic.loadUi('UI/add.ui', self)
        self.username = login
        self.pushButton.clicked.connect(self.addfunction)

    def addfunction(self):
        global connection
        first_name = self.lineEdit.text().toUtf8()
        last_name = self.lineEdit_2.text().toUtf8()
        phone_number = self.lineEdit_3.text().toUtf8()
        birthday = str(self.dateEdit.dateTime().toString('yyyy-MM-dd'))

        if not (first_name and last_name and phone_number):
            error = QMessageBox()
            error.setWindowTitle(u'Ошибка')
            error.setText(u'Все поля должны быть заполнены')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            if not db.add_contact(connection, self.username, first_name, last_name, phone_number, birthday):
                error = QMessageBox()
                error.setWindowTitle(u'Ошибка')
                error.setText(u'Такой контакт уже зарегистрирован')
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
            else:
                success = QMessageBox()
                success.setWindowTitle(u'Успех')
                success.setText(u'Контакт успешно добавлен')
                success.setIcon(QMessageBox.Information)
                success.setStandardButtons(QMessageBox.Ok)
                success.exec_()
                self.close()


class DeleteContact(QWidget):
    def __init__(self, login):
        super(DeleteContact, self).__init__()
        uic.loadUi('UI/delete.ui', self)
        self.username = login
        self.pushButton.clicked.connect(self.delete_item)
        global connection
        contacts = db.get_contacts(connection, self.username)
        for row_data in contacts:
            name = row_data['last_name'] +' '+row_data['first_name']
            phone_number = row_data['phone_number']
            self.listWidget.addItem(_translate("MainWindow", name, None) + ': ' + phone_number)

    def delete_item(self):
        if not self.listWidget.currentItem():
            error = QMessageBox()
            error.setWindowTitle(u'Ошибка')
            error.setText(u'Выберите контакт для удаления')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            global connection
            data = self.listWidget.currentItem().text().toUtf8()
            data = str(data).split(': ')
            db.delete_contact(connection, self.username, data[0], data[1])
            success = QMessageBox()
            success.setWindowTitle(u'Успех')
            success.setText(u'Контакт успешно удален')
            success.setIcon(QMessageBox.Information)
            success.setStandardButtons(QMessageBox.Ok)
            success.exec_()
            self.close()


class EditContact(QWidget):
    def __init__(self, login):
        super(EditContact, self).__init__()
        uic.loadUi('UI/edit.ui', self)
        self.username = login
        self.listWidget.itemClicked.connect(self.item_clicked)
        self.pushButton.clicked.connect(self.edit_item)
        global connection
        contacts = db.get_contacts(connection, self.username)
        for row_data in contacts:
            name = row_data['last_name'] +' '+row_data['first_name']
            phone_number = row_data['phone_number']
            self.listWidget.addItem(_translate("MainWindow", name, None) + ': ' + phone_number)

    def item_clicked(self, item):
        data = self.listWidget.currentItem().text().toUtf8()
        data = str(data).split(': ')
        contact_info = db.find_contact(connection, self.username, data[0], data[1])
        self.lineEdit.setText(_translate("MainWindow", contact_info['first_name'], None))
        self.lineEdit_2.setText(_translate("MainWindow", contact_info['last_name'], None))
        self.lineEdit_3.setText(contact_info['phone_number'])
        self.dateEdit.setDate(contact_info['birthday'])

        self.contact_id = contact_info['id']

    def edit_item(self):
        global connection
        first_name = self.lineEdit.text().toUtf8()
        last_name = self.lineEdit_2.text().toUtf8()
        phone_number = str(self.lineEdit_3.text())
        birthday = str(self.dateEdit.dateTime().toString('yyyy-MM-dd'))

        if not (first_name and last_name and phone_number):
            error = QMessageBox()
            error.setWindowTitle(u'Ошибка')
            error.setText(u'Выберите контакт для редактирования')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            db.edit_contact(connection, self.username, self.contact_id, first_name, last_name, phone_number, birthday)
            success = QMessageBox()
            success.setWindowTitle(u'Успех')
            success.setText(u'Контакт успешно изменен')
            success.setIcon(QMessageBox.Information)
            success.setStandardButtons(QMessageBox.Ok)
            success.exec_()
            self.close()


SETTINGS = QSettings('app', 'dev')

if not SETTINGS.contains('remember_me'):
    SETTINGS.setValue('remember_me', False)
if not SETTINGS.contains('user'):
    SETTINGS.setValue('user', None)


def application():
    app = QtGui.QApplication(sys.argv)
    window = None
    global SETTINGS
    if SETTINGS.value('remember_me') != False:
        if SETTINGS.value('user') != None:
            username = SETTINGS.value('user').toByteArray()
            window = PhoneBook(username)
        else:
            window = Auth()
    else:
        window = Auth()

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    application()