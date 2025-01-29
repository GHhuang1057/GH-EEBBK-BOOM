# coding: utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication

from loguru import logger
from qfluentwidgets import NavigationItemPosition, FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common import resource


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.homeInterface = HomeInterface(self)
        logger.info("创建homeInterface界面")
        self.settingInterface = SettingInterface(self)
        logger.info("创建settingInterface界面")

        self.connectSignalToSlot()

        self.initNavigation()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

        logger.info("连接信号槽")

    def initNavigation(self):

        self.navigationInterface.setAcrylicEnabled(True)
        self.navigationInterface.setExpandWidth(250)

        self.addSubInterface(
            self.homeInterface, FIF.HOME, "首页", NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )

        logger.info("初始化导航栏")
        self.splashScreen.finish()
        logger.info("关闭启动画面")

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(":/app/images/logo.jpg"))
        self.setWindowTitle("EEBBK BOOM")

        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # 创建启动画面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        logger.info("创建启动画面")

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splashScreen.resize(self.size())
