''' Template数据类型 '''
import cv2
from collections import OrderedDict
from PyQt5 import QtGui


class Template:
    def __init__(self, x=0, y=0, w=0, h=0, name=''):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.pixmap = None  # pixmap，用于显示
        self.cvColorImage = None  # cv彩色图像
        self.threshold = 100  # 二值化阈值

    def load_image(self, cvImage):
        ''' 传入原图，根据坐标截取Mask图片，并生成相应的pixmap、binaryImage、grayImage '''
        if not self.w or not self.h:
            return
        x, y, w, h = self.x, self.y, self.w, self.h
        self.cvColorImage = cvImage[y:y+h, x:x+w, :].copy()
        rgbImage = cv2.cvtColor(self.cvColorImage, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        self.pixmap = QtGui.QPixmap.fromImage(image)

    def to_json(self):
        data = OrderedDict({
            'x': self.x,
            'y': self.y,
            'w': self.w,
            'h': self.h,
            'name': self.name,
            'threshold': self.threshold})
        return data

    @staticmethod
    def from_json(jsondata):
        obj = Template()
        obj.x = jsondata['x']
        obj.y = jsondata['y']
        obj.w = jsondata['w']
        obj.h = jsondata['h']
        obj.name = jsondata['name']
        obj.threshold = jsondata['threshold']
        return obj