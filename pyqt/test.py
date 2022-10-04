import sys
import PyQt5
from PyQt5 import uic
import cv2
import os
import numpy as np
from PyQt5.QtCore import Qt, QRect
import sys
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import random
import json

form_class = uic.loadUiType("./test.ui")[0]

class BoxLabel(PyQt5.QtWidgets.QLabel):
    def __init__(self,parent):
        super(BoxLabel, self).__init__(parent)
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
        self.obj = None
        self.rectangles = []
        
        self.setMouseTracking(True)

    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
         # 
    def mouseReleaseEvent(self,event):
        self.flag = False
        
        
        if self.obj != None :
            rect = QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
            self.rectangles.append((rect,self.obj))
        self.update()
         # 
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
         #  event

    
    def select_Qpen(self, obj, type=Qt.SolidLine ):
        
        
        if obj == 'character' :            
            return QPen(QColor(255,0,0),Qt.SolidLine)
        elif obj == "heart" :
            return QPen(QColor(255,153,221),Qt.SolidLine)
        elif obj == "golden_flower" :
            return QPen(QColor(255,255,0),Qt.SolidLine)
        elif obj == "purple_flower" :
            return QPen(QColor(255,100,255),Qt.SolidLine)
        else:
            return QPen(QColor(0,0,0,0),Qt.SolidLine)

    def paintEvent(self, event):
        super(BoxLabel, self).paintEvent(event)
        if self.flag :
            painter = QPainter(self)
            qbox = QPixmap()

            rect = QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
            
            print(self.obj)
            qpen = self.select_Qpen(self.obj)
            painter.setPen(qpen)
            painter.drawRect(rect)
            
            
        
        self.draw_rects()
        

    def draw_rects(self):
        painter = QPainter(self)
        print("draw")
        for rect,obj in self.rectangles :
            qpen = self.select_Qpen(obj)
            painter.setPen(qpen)
            painter.drawRect(rect)
        


    def save_rectangle(self, img, img_name = "test.png"):
        for rect,obj in self.rectangles :
            img = cv2.rectangle(img, (rect.x(), rect.y()), (rect.height()+rect.x(), rect.width()+rect.y()),(255,0,0))
        
        cv2.imwrite(img_name, img)
    def delete_box(self):
        if len(self.rectangles) != 0:
            self.rectangles.pop()
        self.update()

        

class WindowClass(PyQt5.QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Button_show.clicked.connect(self.btnClick)
        self.List_img.currentItemChanged.connect(self.img_name_Change)        
        self.Label_screen.setCursor(Qt.CrossCursor)
        self.Label_box = BoxLabel(self)
        self.Label_box.setGeometry(QRect(20, 10, 1024, 768))
        self.Label_box.setCursor(Qt.CrossCursor)

        
        self.image_folder = None
        self.box_object = "character"

        
        self.img = None        
        self.rectangles = None

    def keyPressEvent(self, e):
        def isPrintable(key):
            printable = [
                Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
                Qt.Key_5,Qt.Key_6,Qt.Key_7,Qt.Key_8,Qt.Key_9,
                Qt.Key_Q, Qt.Key_W,
                Qt.Key_D, Qt.Key_S
            ]

            if key in printable:
                return True
            else:
                return False

        control = False

        if not control and isPrintable(e.key()):
            if self.image_folder != None :
                if e.text() == 'W' or e.text() == 'w' :
                    self.List_img.setCurrentRow(self.List_img.currentRow()+1)
                    
                elif e.text() == 'Q' or e.text() == 'q' :
                    self.List_img.setCurrentRow(self.List_img.currentRow()-1)
                
                elif e.text() == '1' :
                    self.box_object = "character"
                    self.Label_object.setText(self.box_object)
                    self.Label_box.obj = self.box_object
                elif e.text() == '2' :
                    self.box_object = "heart"
                    self.Label_object.setText(self.box_object)
                    self.Label_box.obj = self.box_object            
                elif e.text() == '3' :
                    self.box_object = "golden_flower"
                    self.Label_object.setText(self.box_object)
                    self.Label_box.obj = self.box_object
                elif e.text() == '4' :
                    self.box_object = "purple_flower"
                    self.Label_object.setText(self.box_object)
                    self.Label_box.obj = self.box_object

                elif e.text() == 'd' or e.text() =='D':
                    self.Label_box.delete_box()
                elif e.text() == 's' or e.text() =='S':
                    self.Label_box.save_rectangle(self.img)

                

    def btnClick(self):
        #https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/

        tmp = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, 'open file')
        if tmp != "" :

            self.image_folder = tmp
            self.List_img.clear()
            for img_name in os.listdir(self.image_folder) :
                self.List_img.addItem(img_name)
            #self.rectangles = np.array()

    def img_name_Change(self):
        if self.List_img.currentItem() != None:
            selected_image = self.image_folder +'/'+ self.List_img.currentItem().text()

            self.img = cv2.imdecode(np.fromfile(selected_image,np.uint8),cv2.IMREAD_COLOR)

            

            qimg = PyQt5.QtGui.QPixmap()
            qimg.load(selected_image)
            
            self.Label_screen.setPixmap(qimg)
            print(selected_image)
            print(self.Label_screen.size())



   
if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    myWindow = WindowClass()
    
    myWindow.show()
    app.exec_()
