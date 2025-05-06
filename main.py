import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit

from map import Map


class Apitask(QMainWindow):
    def __init__(self):
        super().__init__()

        self.map = Map()

        self.is_clicked = False

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(600, 570)
        
        self.setMouseTracking(True)

        self.map_image = QLabel(self)
        self.map_image.resize(600, 450)
        self.map_image.move(0, 0)
        self.map_image.setPixmap(QPixmap('intro.png'))

        self.address_label = QLabel(self)
        self.address_label.resize(600, 20)
        self.address_label.move(0, 450)

        self.geocode_edit = QLineEdit(self)
        self.geocode_edit.resize(398, 48)
        self.geocode_edit.move(1, 471)

        f = self.geocode_edit.font()
        f.setPointSize(18)
        self.geocode_edit.setFont(f)

        self.find_button = QPushButton('Найти', self)
        self.find_button.resize(100, 50)
        self.find_button.move(400, 470)
        self.find_button.clicked.connect(self.find)

        self.reset_button = QPushButton('Сбросить', self)
        self.reset_button.resize(100, 50)
        self.reset_button.move(500, 470)
        self.reset_button.clicked.connect(self.reset_point)

        self.theme_button = QPushButton('Смена темы', self)
        self.theme_button.resize(200, 50)
        self.theme_button.move(0, 520)
        self.theme_button.clicked.connect(self.toggle_dark)

        self.mode_button = QPushButton('Смена режима', self)
        self.mode_button.resize(200, 50)
        self.mode_button.move(200, 520)
        self.mode_button.clicked.connect(self.cycle_map_mode)

        self.postcode_button = QPushButton('Показать почтовый индекс', self)
        self.postcode_button.resize(200, 50)
        self.postcode_button.move(400, 520)
        self.postcode_button.clicked.connect(self.toggle_postcode)

    def update_map(self):
        self.map.save_static_map()
        self.map_image.setPixmap(QPixmap('map.png'))
        # self.update()

    def mousePressEvent(self, event):
        if not self.is_clicked:
            self.update_map()  # TODO: m1 and m2 handling

            self.is_clicked = True

        elif 0 <= event.pos().y() <= 450:
            ll = self.map.get_ll_by_click(event.pos().x(), event.pos().y())

            if event.button() == Qt.MouseButton.LeftButton:
                self.map.find_by_ll(ll[0], ll[1])

            elif event.button() == Qt.MouseButton.RightButton:
                self.map.find_organisation(ll[0], ll[1])
            
            self.address_label.setText(self.map.get_address())

            self.update_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            # print(self.map.scale)
            
            self.map.change_scale(True)

        if event.key() == Qt.Key.Key_PageDown:
            # print(self.map.scale)

            self.map.change_scale(False)

        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_H:
                # print('left')

                self.map.move_horizontally(False)

            if event.key() == Qt.Key.Key_J:
                # print('down')

                self.map.move_vertically(False)

            if event.key() == Qt.Key.Key_K:
                # print('up')

                self.map.move_vertically(True)

            if event.key() == Qt.Key.Key_L:
                # print('right')

                self.map.move_horizontally(True)

        self.update_map()

    def toggle_dark(self):
        self.map.toggle_dark()

        self.update_map()

    def toggle_postcode(self):
        self.map.toggle_postcode()

        self.update_map()

    def cycle_map_mode(self):
        self.map.cycle_map_mode()

        self.update_map()

    def find(self):
        self.map.find(self.geocode_edit.text())
        
        self.address_label.setText(self.map.get_address())

        self.update_map()

    def reset_point(self):
        self.map.reset_point()
        self.address_label.setText('')

        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Apitask()
    ex.show()
    sys.exit(app.exec())
