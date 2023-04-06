import sqlite3
import hashlib
import datetime
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QDialog,QTableWidgetItem,QMainWindow,QMessageBox
from PyQt5.QtSql import *
from PyQt5 import QtCore, QtGui,QtWidgets
from DiplomFinalVersion import Ui_MainWindow
import AddSupplyDialog
import AddDealersDialog
import DeleteDealers
import RegWindow
import RegDialog
import AdminWindow
import DeleteUsers

def pass_decryp(value):
    return hashlib.md5(value.encode()).hexdigest()


def createTableUsers():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    password TEXT,
    fname TEXT,
    lname TEXT,
    work TEXT,
    lastlogin TEXT,
    lastexit TEXT,
    lasttask TEXT,
    status TEXT);
    """)
    conn.commit()
def createTableDealers():
    cur.execute("""CREATE TABLE IF NOT EXISTS dealers(
    company TEXT,
    inn INT,
    ph_nm INT,
    url TEXT,
    date TEXT,
    lastdate TEXT);
    """)
    conn.commit()
def createTableSupply():
    cur.execute("""CREATE TABLE IF NOT EXISTS supply(
    company TEXT,
    type TEXT,
    amount INT,
    price REAL,
    date REAL);
    """)
    conn.commit()

def createTableItems():
    cur.execute("""CREATE TABLE IF NOT EXISTS items(
    type TEXT,
    amount INT,
    datelast TEXT);
    """)
    conn.commit()



conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
cur = conn.cursor()
createTableUsers()
createTableSupply()
createTableDealers()
createTableItems()
user = ''









class MainApp(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.Load_Database_Dealers()
        self.Load_Database_Items()
        self.Load_Database_Supply()
        self.AddDealers()
        self.AddSupply()
        self.DelDealers()
        self.DelSupply()
        self.SearchIt()
        self.SearchCo()
        self.Exit()

    def Exit(self):
        self.show()
        self.exitButton.clicked.connect(self.Exit_Prog)

    def Exit_Prog(self):
        now = datetime.datetime.now()
        cur.execute("UPDATE users SET lastexit = ?, status = 'OFFLINE' WHERE login = ? ", [now, user])
        conn.commit()
        self.close()
        self.opening = RegWindow()
        self.opening.show()

    def SearchCo(self):
        self.show()
        self.searchCoButton.clicked.connect(self.Open_SearchCo)

    def Open_SearchCo(self):
        CO = self.searchCoLine.text()
        CO = '%' + CO + '%'
        if not CO:
            self.Load_Database_Dealers()
            self.Load_Database_Supply()
        else:
            while self.DealersTable.rowCount() > 0:
                self.DealersTable.removeRow(0)
            conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
            cur = conn.cursor()
            res = conn.execute('SELECT * FROM dealers WHERE company LIKE ?', [CO])
            for row_index, row_data in enumerate(res):
                self.DealersTable.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.DealersTable.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

            while self.SupplyTable.rowCount() > 0:
                self.SupplyTable.removeRow(0)
            res = conn.execute('SELECT * FROM supply WHERE company LIKE ?', [CO])
            for row_index, row_data in enumerate(res):
                self.SupplyTable.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.SupplyTable.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
            conn.close()
            return

    def SearchIt(self):
        self.show()
        self.searchItButton.clicked.connect(self.Open_SearchIt)

    def Open_SearchIt(self):
        ITEM =self.searchItLine.text()
        ITEM = '%' + ITEM + '%'
        if not ITEM:
            self.Load_Database_Items()
        else:
            while self.ItemsTable.rowCount() > 0:
                self.ItemsTable.removeRow(0)
            conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
            cur = conn.cursor()
            res = conn.execute('SELECT * FROM items WHERE type LIKE ?', [ITEM])
            for row_index, row_data in enumerate(res):
                self.ItemsTable.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.ItemsTable.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
            conn.close()
            return






    def AddDealers(self):
        self.show()
        self.dPlusButton.clicked.connect(self.Show_addD_Dialog)

    def Show_addD_Dialog(self):
        self.adding=addDDialog()
        self.adding.dOKButton.clicked.connect(self.Add_DataD)
        self.adding.dClearButton.clicked.connect(self.ClearLinesD)
        self.adding.exec_()

    def ClearLinesD(self):
        self.adding.NLine.clear()
        self.adding.INNLine.clear()
        self.adding.SiteLine.clear()
        self.adding.TelLine.clear()
        self.adding.FLine.clear()



    def Add_DataD(self):
        COMPANY = self.adding.NLine.text()
        INN = self.adding.INNLine.text()
        PH_NM = self.adding.SiteLine.text()
        URL = self.adding.TelLine.text()
        DATE = self.adding.FLine.text()
        try:
            if COMPANY =='' or INN =='' or PH_NM =='' or DATE =='':
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Некорректные данные")
                box.exec_()
            else:
                cur.execute("SELECT company FROM dealers WHERE company = ?", [COMPANY])
                if cur.fetchone() is None:
                    new_user = [COMPANY, INN, PH_NM, URL, DATE, DATE]
                    cur.execute("INSERT INTO dealers VALUES (?, ?, ?, ?, ?, ?)",new_user)
                    conn.commit()
                    cur.execute("UPDATE users SET lasttask = 'Добавил поставщика' WHERE login = ? ", [user])
                    conn.commit()
                    now = datetime.datetime.now()
                    cur.execute("UPDATE users SET lastexit = ? WHERE login = ? ", [now, user])
                    conn.commit()
                    self.adding.close()
                else:
                    box = QMessageBox()
                    box.setWindowTitle("Ошибка")
                    box.setText("Компания уже зарегестрирована")
                    box.exec_()

        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            self.Load_Database_Dealers()









    def DelDealers(self):
        self.show()
        self.dDelButton.clicked.connect(self.Show_delD_Dialog)

    def Show_delD_Dialog(self):
        self.deleting = delDDialog()
        self.deleting.DelDOKButto.clicked.connect(self.Del_DataD)
        self.deleting.DelDClearButton.clicked.connect(self.ClearLinesDDel)
        self.deleting.exec_()

    def ClearLinesDDel(self):
        self.deleting.compLineD.clear()

    def Del_DataD(self):
        COMPANY = self.deleting.compLineD.text()
        try:
            cur.execute("SELECT* FROM dealers WHERE company=? ",[COMPANY])
            if cur.fetchone() is None:
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Компания не зарегестрирована")
                box.exec_()
            else:
                cur.execute("UPDATE users SET lasttask = 'Удалил поставщика' WHERE login = ? ", [user])
                conn.commit()
                now = datetime.datetime.now()
                cur.execute("UPDATE users SET lastexit = ? WHERE login = ? ", [now,user])
                conn.commit()
                cur.execute("DELETE FROM dealers WHERE company = ?", [COMPANY])
                conn.commit()
                self.deleting.close()
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            self.Load_Database_Dealers()








    def AddSupply(self):
        self.show()
        self.sPlusButton.clicked.connect(self.Show_addS_Dialog)

    def Show_addS_Dialog(self):
        self.adding = addSDialog()
        self.adding.sOKButton.clicked.connect(self.Add_DataS)
        self.adding.sClearButton.clicked.connect(self.ClearLinesS)
        self.adding.exec_()

    def ClearLinesS(self):
        self.adding.comLine.clear()
        self.adding.typeLine.clear()
        self.adding.amountLine.clear()
        self.adding.priceLine.clear()
        self.adding.dateLine.clear()

    def Add_DataS(self):
        COMPANY = self.adding.comLine.text()
        TYPE = self.adding.typeLine.text()
        AMOUNT = self.adding.amountLine.text()
        PRICE = self.adding.priceLine.text()
        DATE = self.adding.dateLine.text()
        try:
            if COMPANY == '' or TYPE =='' or AMOUNT =='' or PRICE =='' or DATE == '':
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Некорректные данные")
                box.exec_()
            else:
                cur.execute("UPDATE users SET lasttask = 'Добавил поставку' WHERE login = ? ", [user])
                conn.commit()
                now = datetime.datetime.now()
                cur.execute("UPDATE users SET lastexit = ? WHERE login = ? ", [now, user])
                conn.commit()
                cur.execute("SELECT company FROM dealers WHERE company = ?",[COMPANY])
                if cur.fetchone() is None:
                    box = QMessageBox()
                    box.setWindowTitle("Ошибка")
                    box.setText("Компания не зарегестрирована")
                    box.exec_()
                else:
                    new_sup = [COMPANY, TYPE, AMOUNT, PRICE, DATE]
                    cur.execute("INSERT INTO supply (company,type ,amount ,price ,date) VALUES ( ?, ?, ?, ?, ?)",new_sup)
                    cur.execute("UPDATE dealers SET lastdate=? WHERE company = ?",[DATE,COMPANY])
                    cur.execute("UPDATE users SET lasttask = 'Добавил поставку ' WHERE login = ? ", [COMPANY, user])
                    conn.commit()
                    cur.execute("SELECT type FROM items WHERE type = ?", [TYPE])
                    if cur.fetchone() is None:
                        new_item=[TYPE,AMOUNT,DATE]
                        cur.execute("INSERT INTO items (type ,amount ,datelast) VALUES (?, ?, ?)", new_item)
                        conn.commit()
                        self.adding.close()
                    else:
                        cur.execute("UPDATE items SET datelast=?,amount=amount+? WHERE type = ?",[DATE,AMOUNT,TYPE])
                        conn.commit()
                        self.adding.close()
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            self.Load_Database_Supply()
            self.Load_Database_Dealers()
            self.Load_Database_Items()




    def DelSupply(self):
        self.show()
        self.sDelButton.clicked.connect(self.Del_DataS)

    def Del_DataS(self):
        cur.execute("SELECT * FROM supply")
        if cur.fetchone() is None:
            box = QMessageBox()
            box.setWindowTitle("Ошибка")
            box.setText("Таблица пуста")
            box.exec_()
        else:
            rowCount = self.SupplyTable.rowCount()
            COMPANY = self.SupplyTable.item(rowCount - 1, 0).text()
            TYPE = self.SupplyTable.item(rowCount - 1, 1).text()
            AMOUNT = self.SupplyTable.item(rowCount - 1, 2).text()
            now = datetime.datetime.now()
            cur.execute("UPDATE users SET lastexit = ? WHERE login = ? ", [now, user])
            conn.commit()
            cur.execute("UPDATE users SET lasttask = 'Удалил поставку ' WHERE login = ? ", [COMPANY,user])
            conn.commit()
            cur.execute("SELECT * FROM supply WHERE type = "
                        "(SELECT type FROM supply WHERE rowid = "
                        "(SELECT MAX(rowid) FROM supply)) AND rowid <(SELECT MAX(rowid) FROM supply) ")
            if cur.fetchone() is None:
                cur.execute("DELETE FROM supply WHERE rowid=(SELECT MAX(rowid) FROM supply)")
                cur.execute("DELETE FROM items WHERE rowid=(SELECT MAX(rowid) FROM items)")
                conn.commit()
                self.Load_Database_Supply()
                self.Load_Database_Items()
            else:
                cur.execute("DELETE FROM supply WHERE rowid=(SELECT MAX(rowid) FROM supply)")
                cur.execute("UPDATE items SET amount = amount -? WHERE type = ?", [AMOUNT, TYPE])
                cur.execute("UPDATE items SET datelast = "
                            "(SELECT date FROM supply WHERE type = ? AND rowid = "
                            "(SELECT MAX(rowid) FROM supply WHERE type=?))",[TYPE,TYPE])
                conn.commit()
                self.Load_Database_Supply()
                self.Load_Database_Items()
            cur.execute("SELECT date FROM supply WHERE company = ?", [COMPANY])
            if cur.fetchone() is None:
                cur.execute("UPDATE dealers SET lastdate = date WHERE company = ? ", [COMPANY])
                conn.commit()
                self.Load_Database_Dealers()
            else:
                cur.execute(
                    "UPDATE dealers SET lastdate = (SELECT date FROM supply WHERE rowid = (SELECT MAX(rowid) from supply WHERE company=?)) "
                    "WHERE company = ? ", [COMPANY, COMPANY])
                conn.commit()
                self.Load_Database_Dealers()






    def Load_Database_Supply(self):
        while self.SupplyTable.rowCount()>0:
            self.SupplyTable.removeRow(0)
        conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
        cur = conn.cursor()
        content='SELECT * FROM supply'
        res=conn.execute(content)
        for row_index ,row_data in enumerate(res):
            self.SupplyTable.insertRow(row_index)
            for col_index,col_data in enumerate(row_data):
                self.SupplyTable.setItem(row_index,col_index,QTableWidgetItem(str(col_data)))
        conn.close()
        return




    def Load_Database_Items(self):
        while self.ItemsTable.rowCount()>0:
            self.ItemsTable.removeRow(0)
        conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
        cur = conn.cursor()
        content='SELECT * FROM items'
        res=conn.execute(content)
        for row_index ,row_data in enumerate(res):
            self.ItemsTable.insertRow(row_index)
            for col_index,col_data in enumerate(row_data):
                self.ItemsTable.setItem(row_index,col_index,QTableWidgetItem(str(col_data)))
        conn.close()
        return



    def Load_Database_Dealers(self):
        while self.DealersTable.rowCount()>0:
            self.DealersTable.removeRow(0)
        conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
        cur = conn.cursor()
        content='SELECT * FROM dealers'
        res=conn.execute(content)
        for row_index ,row_data in enumerate(res):
            self.DealersTable.insertRow(row_index)
            for col_index,col_data in enumerate(row_data):
                self.DealersTable.setItem(row_index,col_index,QTableWidgetItem(str(col_data)))
        conn.close()
        return



class addSDialog(QDialog,AddSupplyDialog.Ui_Dialog):
    def __init__(self,parent=None):
        super(addSDialog, self).__init__(parent)
        self.setupUi(self)

class addDDialog(QDialog,AddDealersDialog.Ui_Dialog):
    def __init__(self,parent=None):
        super(addDDialog, self).__init__(parent)
        self.setupUi(self)

class delDDialog(QDialog,DeleteDealers.Ui_Dialog):
    def __init__(self,parent=None):
        super(delDDialog, self).__init__(parent)
        self.setupUi(self)

class RegDialog(QDialog,RegDialog.Ui_Dialog):
    def __init__(self,parent=None):
        super(RegDialog, self).__init__(parent)
        self.setupUi(self)


class RegWindow(QMainWindow,RegWindow.Ui_MainWindow):
    def __init__(self,parent=None):
        super(RegWindow, self).__init__(parent)
        self.setupUi(self)
        self.User_Interface()

    def User_Interface(self):
        self.show()
        self.regButton.clicked.connect(self.regU)
        self.logButton.clicked.connect(self.logU)

    def regU(self):
        self.adding=RegDialog()
        self.adding.show()
        self.adding.regButton.clicked.connect(self.REG)

    def REG(self):
        LOGIN = self.adding.loginLine.text()
        PASSWORD = self.adding.passLine.text()
        PASSWORD2 = self.adding.passAgainLine.text()
        FNAME = self.adding.fNameLine.text()
        LNAME = self.adding.lNameLine.text()
        WORK= self.adding.workLine.text()
        try:
            if LOGIN == '' or PASSWORD =='' or PASSWORD2 =='' or FNAME =='' or LNAME == '' or WORK =='':
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Некорректные данные")
                box.exec_()
            elif PASSWORD2!=PASSWORD:
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Пароли не совпадают")
                box.exec_()
            else:
                conn.create_function("hash", 1, pass_decryp)
                cur.execute("SELECT login FROM users WHERE login = ?", [LOGIN])
                if cur.fetchone() is None:
                    new_user = [LOGIN,PASSWORD,FNAME,LNAME,WORK]
                    cur.execute("INSERT INTO users(login ,password,fname,lname,work) VALUES ( ?, hash(?), ?, ?,? )",
                                new_user)
                    conn.commit()
                    self.adding.close()
                else:
                    box = QMessageBox()
                    box.setWindowTitle("Ошибка")
                    box.setText("Пользователь с таким логином уже зарегестрирован")
                    box.exec_()
        except sqlite3.Error as e:
            print("Error:", e)

    def logU(self):
        LOGIN = self.logLine.text()
        PASSWORD = self.passLine.text()
        try:
            conn.create_function("hash", 1, pass_decryp)
            cur.execute("SELECT login FROM users WHERE login = ?", [LOGIN])
            if cur.fetchone() is None:
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Неправильный логин ил пароль")
                box.exec_()
            else:
                cur.execute("SELECT password FROM users WHERE login = ? AND password=hash(?)", [LOGIN, PASSWORD])
                if cur.fetchone() is None:
                    box = QMessageBox()
                    box.setWindowTitle("Ошибка")
                    box.setText("Неправильный логин ил пароль")
                    box.exec_()
                else:
                    global user
                    user = LOGIN
                    now = datetime.datetime.now()
                    cur.execute("UPDATE users SET lastlogin = ?, status = 'ONLINE' WHERE login = ? ", [now, user])
                    conn.commit()
                    cur.execute("SELECT work FROM users WHERE login=? and work='Администратор'",[LOGIN])
                    if cur.fetchone() is None:
                        self.close()
                        self.oppening = MainApp()
                        self.oppening.show()
                    else:
                        self.close()
                        self.oppening = AdminWindow()
                        self.oppening.show()
        except sqlite3.Error as e:
            print("Error:", e)


class AdminWindow(QMainWindow,AdminWindow.Ui_MainWindow):
    def __init__(self,parent=None):
        super(AdminWindow, self).__init__(parent)
        self.setupUi(self)
        self.Admin_Interface()
        self.Load_Database_Users()
        self.Find_User()


    def Admin_Interface(self):
        self.show()
        self.delUser.clicked.connect(self.delUserA)
        self.addUser.clicked.connect(self.addUserA)
        self.searchButton.clicked.connect(self.findUserA)
        self.exitButton.clicked.connect(self.Exit)

    def Exit(self):
        self.exiting=RegWindow()
        self.close()
        self.exiting.show()

    def addUserA(self):
        self.adding = RegDialog()
        self.adding.show()
        self.adding.regButton.clicked.connect(self.Add_User)
        self.adding.exec_()

    def Add_User(self):
        LOGIN = self.adding.loginLine.text()
        PASSWORD = self.adding.passLine.text()
        PASSWORD2 = self.adding.passAgainLine.text()
        FNAME = self.adding.fNameLine.text()
        LNAME = self.adding.lNameLine.text()
        WORK = self.adding.workLine.text()
        try:
            if LOGIN == '' or PASSWORD == '' or PASSWORD2 == '' or FNAME == '' or LNAME == '' or WORK == '':
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Некорректные данные")
                box.exec_()
            elif PASSWORD2 != PASSWORD:
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Пароли не совпадают")
                box.exec_()
            else:
                conn.create_function("hash", 1, pass_decryp)
                cur.execute("SELECT login FROM users WHERE login = ?", [LOGIN])
                if cur.fetchone() is None:
                    new_user = [LOGIN, PASSWORD, FNAME, LNAME, WORK]
                    cur.execute("INSERT INTO users(login ,password,fname,lname,work) VALUES ( ?, hash(?), ?, ?,? )",
                                new_user)
                    conn.commit()
                    self.adding.close()
                    self.Load_Database_Users()
                else:
                    box = QMessageBox()
                    box.setWindowTitle("Ошибка")
                    box.setText("Пользователь с таким логином уже зарегестрирован")
                    box.exec_()
        except sqlite3.Error as e:
            print("Error:", e)




    def delUserA(self):
        self.deleting=delUsersDialog()
        self.deleting.show()
        self.deleting.okButton.clicked.connect(self.OKU)
        self.deleting.clearButton.clicked.connect(self.ClearLineU)

    def OKU(self):
        LOGIN = self.deleting.loginLine.text()
        try:
            cur.execute("SELECT* FROM users WHERE login=? ", [LOGIN])
            if cur.fetchone() is None:
                box = QMessageBox()
                box.setWindowTitle("Ошибка")
                box.setText("Пользователь не зарегестрирован")
                box.exec_()
            else:
                cur.execute("DELETE FROM users WHERE login = ?", [LOGIN])
                conn.commit()
                self.deleting.close()
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            self.Load_Database_Users()

    def ClearLineU(self):
        self.show()
        self.deleting.loginLine.clear()


    def Find_User(self):
        self.show()
        self.searchButton.clicked.connect(self.findUserA)


    def findUserA(self):
        LN = self.searchLine.text()
        LN = '%' + LN + '%'
        if not LN:
            self.Load_Database_Users()
        else:
            while self.userTable.rowCount() > 0:
                self.userTable.removeRow(0)
            conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
            cur = conn.cursor()
            res = conn.execute('SELECT * FROM users WHERE login LIKE ? AND work!="Администратор"', [LN])
            for row_index, row_data in enumerate(res):
                self.userTable.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.userTable.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
            conn.close()
            return

aaaaaaaaaaaaaaaaaaa
    def Load_Database_Users(self):
        while self.userTable.rowCount() > 0:
            self.userTable.removeRow(0)
        conn = sqlite3.connect(r'/Users/nikitaavilkin/Desktop/DataBase/DATABASE.db')
        cur = conn.cursor()
        res = conn.execute('SELECT * FROM users WHERE work!="Администратор"')
        for row_index, row_data in enumerate(res):
            self.userTable.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.userTable.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        conn.close()
        return





class delUsersDialog(QMainWindow,DeleteUsers.Ui_Dialog):
    def __init__(self,parent=None):
        super(delUsersDialog, self).__init__(parent)
        self.setupUi(self)









app = QApplication([])
window=RegWindow()
app.exec()










