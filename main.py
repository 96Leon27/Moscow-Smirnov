import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        connection = sqlite3.connect("coffee.sqlite")
        cur = connection.cursor()

        res = cur.execute('SELECT * FROM coffee').fetchall()

        titles = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                  'описание вкуса', 'цена (₽)', 'объем упаковки (кг)']
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(len(res))

        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
