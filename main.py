import random
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QColor, QPainter
from random import randint
from UI import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.paint)
        self.do_paint = False
        self.circles = []

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            for i in self.circles:
                qp.setPen(i[0])
                qp.drawEllipse(*i[1:])
            qp.end()
        self.do_paint = False

    def paint(self):
        self.do_paint = True
        r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
        color = QColor(r, g, b)
        r = random.randint(5, 250)
        center_x = random.randint(0, 500 - r) + r // 2
        center_y = random.randint(0, 500 - r) + r // 2
        self.circles.append([color, center_x, center_y, r, r])
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
