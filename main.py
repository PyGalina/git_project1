import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
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

    def run(self):
        self.model.setTable('coffee')
        self.model.select()
        self.view.setModel(self.model)
    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyCoffee()
    ex.show()
    sys.exit(app.exec())
