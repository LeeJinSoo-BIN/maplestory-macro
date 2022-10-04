import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 500, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("/test_img/2.png")
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() -10 , 10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())