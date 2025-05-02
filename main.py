import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class Apitask(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 500, 500)
        
        self.setMouseTracking(True)

        self.button = QPushButton('Смена темы', self)
        self.button.resize(100, 50)
        self.button.move(150, 250)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Apitask()
    ex.show()
    sys.exit(app.exec())