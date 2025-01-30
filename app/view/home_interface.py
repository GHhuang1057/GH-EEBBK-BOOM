# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from loguru import logger
from qfluentwidgets import SmoothScrollArea

from ..components.flow_layout import FlowLayout
from ..components.disclaimer_card import DisclaimerCard


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


class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)

        self.disclaimerCard = DisclaimerCard(self)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName("HomeInterface")
        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.addWidget(self.disclaimerCard, 0, Qt.AlignmentFlag.AlignTop)
      
