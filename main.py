import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class MyCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()
        self.model = QSqlTableModel(self, db)
        self.runbtn.clicked.connect(self.run)
        self.editbtn.clicked.connect(self.open_edit)

    def open_edit(self):
        self.editform = EditForm(self)
        self.editform.show()

    def run(self):
        self.model.setTable('coffee')
        self.model.select()
        self.view.setModel(self.model)


class EditForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.editButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.append_new)
        self.pushButton_4.clicked.connect(self.save_new)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE name_sort=?",
                             (name := self.textEdit.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            QMessageBox.information(
                self,
                'Информация',
                'Ничего не нашлось',
                QMessageBox.StandardButton.Ok)
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Спень обжарки', 'Молотый/в зернах', 'Описание', 'Цена', 'Объем'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE name_sort = ?"
            #  print(que)
            cur.execute(que, (self.textEdit.text(),))
            self.con.commit()
            self.modified.clear()

    def append_new(self):
        cur = self.con.cursor()
        self.modified = {}
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(7)
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Спень обжарки', 'Молотый/в зернах', 'Описание', 'Цена', 'Объем'])

    def save_new(self):
        if self.modified:
            cur = self.con.cursor()
            que = "INSERT INTO coffee("
            que += ", ".join([f"{key}" for key in self.modified.keys()])
            que += ') VALUES ('
            que += ",".join([f"'{self.modified.get(key)}'"
                             for key in self.modified.keys()])
            que += ')'
            #  print(que)
            cur.execute(que)
            self.con.commit()
            self.modified.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyCoffee()
    ex.show()
    sys.exit(app.exec())
