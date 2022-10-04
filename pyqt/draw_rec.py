from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2
import sys
class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    # 
    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
         # 
    def mouseReleaseEvent(self,event):
        self.flag = False
         # 
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
         #  event
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
        qbox = QPixmap()
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(675, 300)
        self.setWindowTitle('Draw a rectangle in the label')
        self.lb = MyLabel(self) #redefine label
        self.lb.setGeometry(QRect(30, 30, 511, 541))
        img = cv2.imread('./test_img/2.png')
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine,QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.lb.setPixmap(pixmap)

        self.lb.setCursor(Qt.CrossCursor)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())