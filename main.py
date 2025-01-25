import random
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QColor, QPainter
from random import randint


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.pushButton.clicked.connect(self.paint)
        self.color = QColor('yellow')
        self.do_paint = False
        self.circles = []

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            qp.setPen(self.color)
            for i in self.circles:
                qp.drawEllipse(*i)
            qp.end()
        self.do_paint = False

    def paint(self):
        self.do_paint = True
        r = random.randint(5, 250)
        center_x = random.randint(0, 500 - r) + r // 2
        center_y = random.randint(0, 500 - r) + r // 2
        self.circles.append([center_x, center_y, r, r])
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
