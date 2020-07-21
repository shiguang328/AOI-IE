import os
from PyQt5 import QtCore, QtGui, QtWidgets
from template_widget_ui import Ui_Form
from template import Template


class TemplateWidget(QtWidgets.QWidget, Ui_Form):

    savePatternSignal = QtCore.pyqtSignal(name='savePatternSignal')  # 保存pattern
    selectedChanged = QtCore.pyqtSignal(str, str, name='selectedChanged')
    parameterChanged = QtCore.pyqtSignal(name='parameterChanged')  # 任何程式相关的参数变化后都必须触发该信号告知父类pattern已被修改

    def __init__(self):
        ''' Template页面 '''
        super().__init__()
        self.setupUi(self)
        self.threshSlider.setRange(0, 255)
        self.threshSlider.sliderMoved.connect(self.threshold_changed)
        self.previewLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.currentTemplate = None
        self.templateList = []
        self.saveButton.clicked.connect(self.savePatternSignal)
        self.listWidget.currentRowChanged.connect(self.item_changed)

    def set_template(self, template):
        self.currentTemplate = template
        self.threshSlider.setValue(self.currentTemplate.threshold)
        pixmap = self.currentTemplate.pixmap.scaled(self.previewLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.previewLabel.setPixmap(pixmap)

    def delete_by_name(self, name=''):
        index = -1
        for i, template in enumerate(self.templateList):
            if template.name == name:
                index = i
                break
        if index >= 0:
            self.templateList.pop(index)
            # self.listWidget.takeItem(index)  # remove row from qlistwidget
            self.update_listwidget()

    def threshold_changed(self, value):
        ''' 拖动slider后的响应函数，更新图片显示 '''
        if not self.currentTemplate:
            return
        # pixmap = self.currentTemplate.binary_threshold_changed(value)
        # pixmap = pixmap.scaled(self.previewLabel.size(), QtCore.Qt.KeepAspectRatio)
        # self.previewLabel.setPixmap(pixmap)
        self.parameterChanged.emit()

    def update_pixmap_show(self):
        if self.currentTemplate:
            pixmap = self.currentTemplate.pixmap.scaled(self.previewLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.previewLabel.setPixmap(pixmap)
            self.selectedChanged.emit('template', self.currentTemplate.name)

    def save_current(self):
        if not self.currentTemplate and not self.templateList:
            QtWidgets.QMessageBox.warning(self, '提示', '请先选择一个template')
            return
        elif self.currentTemplate and self.currentTemplate not in self.templateList:  # 新保存
            self.templateList.append(self.currentTemplate)
            self.currentTemplate = None
            self.update_listwidget()
            count = self.listWidget.count()
            self.listWidget.setCurrentRow(count-1)
            # print('add new template')
        else:  # 修改, TODO
            pass
        # self.savePatternSignal.emit()

    def update_listwidget(self):
        self.listWidget.clear()
        # for i in range(len(self.templateList)):
        #     self.listWidget.addItem('template_{}'.format(i+1))
        for template in self.templateList:
            self.listWidget.addItem(template.name)
        if self.templateList:
            self.listWidget.setCurrentRow(0)  # 显示第一个template
            self.threshSlider.setValue(self.templateList[0].threshold)
            # self.item_changed(0)  # 显示第一个template
            # self.selectedChanged.emit('template', self.currentTemplate.name)

    def item_changed(self, rowIndex):
        self.currentTemplate = self.templateList[rowIndex]
        pixmap = self.currentTemplate.pixmap
        pixmap = pixmap.scaled(self.previewLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.previewLabel.setPixmap(pixmap)
        self.selectedChanged.emit('template', self.currentTemplate.name)

    def set_current_template_by_name(self, name):
        for i, template in enumerate(self.templateList):
            if template.name == name:
                # self.listWidget.setCurrentIndex(i)
                self.listWidget.setCurrentRow(i)
                return