# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from loguru import logger
from qfluentwidgets import SmoothScrollArea

from ..components.flow_layout import FlowLayout


# 瀑布流布局,用于加载功能板块
class HomeScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgets = QWidget(self)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName("HomeScrollArea")
        self.setWidgetResizable(True)
        self.setWidget(self.widgets)
        self.setStyleSheet(
            "#HomeScrollArea{" "background:transparent;" "border:none;" "}"
        )

        self.widgets.setObjectName("HomeScrollAreaWidget")
        self.widgets.setStyleSheet(
            "#HomeScrollAreaWidget{"
            "background:transparent;"
            "background-color:#F7F9FC;"
            "}"
        )

        self.__initLayout()

    def __initLayout(self):
        self.layouts = FlowLayout(self.widgets)
        self.layouts.setContentsMargins(0, 5, 0, 5)
        self.widgets.setLayout(self.layouts)
    
    def addSubWidget(self, widget) -> None:
        """
        addSubWidget 添加子控件到流式布局中
        Args:
            widget (QWidget): 添加到流式布局的字控件
        """
        self.layouts.addWidget(widget)


# Home页面
#这里是我(huang1057)修改的
#添加了一个布局
#如果代码不能运行，就把以下的注释恢复
#class HomeInterface(QWidget):
    #def __init__(self, parent=None):
        #super().__init__(parent=parent)
        #self.__initWidget()

    #def __initWidget(self):
        #self.setObjectName("HomeInterface")

        #self.__initLayout()

    #def __initLayout(self):
        #pass


class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__initWidget()

    def __initWidget(self):
        self.setObjectName("HomeInterface")
        self.__initLayout()

    def __initLayout(self):
        # 创建一个垂直布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.main_layout.setSpacing(0)  # 设置布局中控件之间的间距

        # 创建 HomeScrollArea 并将其添加到主布局中
        self.scroll_area = HomeScrollArea(self)
        self.main_layout.addWidget(self.scroll_area)
