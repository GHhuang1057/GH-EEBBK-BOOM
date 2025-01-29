# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ..common.setFont import setFont, FontWeight

from qfluentwidgets import CardWidget, BodyLabel

class ConnectionInformationCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.hBoxLayout = QHBoxLayout(self)
        
        self.connectDevices = BodyLabel(self)
        
        self.__initWidget()
    
    def __initWidget(self):

        self.__initLayout()

    def __initLayout(self):
        pass
