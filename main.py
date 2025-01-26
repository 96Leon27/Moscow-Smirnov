import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.addButton.clicked.connect(self.add)
        self.changeButton.clicked.connect(self.change)
        self.upd()

    def upd(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()

        res = cur.execute('SELECT * FROM coffee').fetchall()

        titles = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                  'описание вкуса', 'цена (₽)', 'объем упаковки (кг)']
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(len(res))

        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()

    def add(self):
        self.add_coffee_widget = AddCoffeeWidget(self)
        self.add_coffee_widget.show()

    def change(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 0:
            self.statusbar.showMessage('Ничего не выбрано')
            return
        if len(ids) != 1:
            self.statusbar.showMessage('Слишком много элементов выделено')
            return
        self.change_coffee_widget = AddCoffeeWidget(self, ids[0])
        self.change_coffee_widget.show()


class AddCoffeeWidget(QMainWindow):
    def __init__(self, parent=None, film_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.film_id = film_id
        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        if self.film_id is not None:
            self.pushButton.setText('Отредактировать')
            self.setWindowTitle('Редактирование записи')
            self.get_elem()  # метод, заполняющий форму
        else:
            self.setWindowTitle('Добавление записи')
        self.pushButton.clicked.connect(self.edit_elem)

    def get_elem(self):
        result = self.cur.execute(f"""SELECT * FROM coffee WHERE ID = {self.film_id}""").fetchall()
        self.sort_edit.setText(f'{result[0][1]}')
        self.degree_of_roasting_edit.setText(f'{result[0][2]}')
        self.type_edit.setText(f'{result[0][3]}')
        self.description_edit.setPlainText(f'{result[0][4]}')
        self.price_edit.setText(f'{result[0][5]}')
        self.volume_edit.setText(f'{result[0][6]}')

    def edit_elem(self):
        try:
            sort = self.sort_edit.text()
            degree_of_roasting = int(self.degree_of_roasting_edit.text())
            tp = self.type_edit.text()
            description = self.description_edit.toPlainText()
            price = float(self.price_edit.text())
            volume = float(self.volume_edit.text())
        except ValueError:
            self.statusbar.showMessage('Неверно заполнена форма')
            return
        if not all([sort, degree_of_roasting, tp, description, price, volume]):
            self.statusbar.showMessage('Неверно заполнена форма')
            return
        if self.film_id is None:
            result = self.cur.execute(f"""
            INSERT INTO coffee (sort,
            "degree of roasting",
            type,
            description,
            price,
            volume) VALUES
                ('{sort}', {degree_of_roasting}, '{tp}', '{description}', {price}, {volume})""").fetchall()
            self.add = True
        else:
            print()
            result = self.cur.execute(f"""
            UPDATE coffee
            SET sort = '{sort}',
                "degree of roasting" = {degree_of_roasting},
                type = '{tp}',
                description = '{description}',
                price = {price},
                volume = {volume}
            WHERE ID = {self.film_id}
            """).fetchall()
            self.edit = True
        self.con.commit()
        self.parent().upd()
        self.close()

    def get_adding_verdict(self):
        return self.add

    def get_editing_verdict(self):
        return self.edit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
