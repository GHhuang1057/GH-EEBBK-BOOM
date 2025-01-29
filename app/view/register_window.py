# coding:utf-8
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout

from loguru import logger
from qfluentwidgets import (
    MSFluentTitleBar,
    isDarkTheme,
    ImageLabel,
    BodyLabel,
    LineEdit,
    PasswordLineEdit,
    PrimaryPushButton,
    CheckBox,
    InfoBar,
    InfoBarPosition,
    setThemeColor,
    HyperlinkButton,
)
from ..common import resource
from ..common.license_service import LicenseServiceThread
from ..common.config import cfg
from .main_window import MainWindow


def isWin11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class RegisterWindow(Window):
    """Register window"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        setThemeColor("#28afe9")
        self.setTitleBar(MSFluentTitleBar(self))

        self.imageLabel = ImageLabel(":/app/images/background.png", self)
        self.iconLabel = ImageLabel(":/app/images/logo.jpg", self)

        self.qqLabel = BodyLabel("QQ号", self)
        self.qqLineEdit = LineEdit(self)

        self.activateCodeLabel = BodyLabel("激活码", self)
        self.activateCodeLineEdit = PasswordLineEdit(self)

        self.rememberCheckBox = CheckBox("记住我", self)

        self.loginButton = PrimaryPushButton("登录", self)
        self.urlButton = HyperlinkButton(
            "https://www.eebbk.com.cn/", "跳转EEBBK BOOM官网", self
        )

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.__initWidgets()
        logger.info("初始化登录窗口")

    def __initWidgets(self):
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        self.rememberCheckBox.setChecked(cfg.get(cfg.rememberMe))

        self.qqLineEdit.setPlaceholderText("0000000000")
        self.activateCodeLineEdit.setPlaceholderText("••••••••••••")

        if self.rememberCheckBox.isChecked():
            self.qqLineEdit.setText(cfg.get(cfg.email))
            self.activateCodeLineEdit.setText(cfg.get(cfg.activationCode))

        self.__connectSignalToSlot()
        self.__initLayout()

        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            color = QColor(25, 33, 42) if isDarkTheme() else QColor(240, 244, 249)
            self.setStyleSheet(f"RegisterWindow{{background: {color.name()}}}")

        self.setWindowTitle("EEBBK BOOM")
        self.setWindowIcon(QIcon(":/app/images/logo.jpg"))
        self.resize(1000, 650)

        self.titleBar.titleLabel.setStyleSheet(
            """
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """
        )

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.titleBar.raise_()

    def __initLayout(self):
        self.imageLabel.scaledToHeight(650)
        self.iconLabel.scaledToHeight(100)

        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout.setSpacing(0)
        self.hBoxLayout.setSpacing(0)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addSpacing(38)
        self.vBoxLayout.addWidget(self.qqLabel)
        self.vBoxLayout.addSpacing(11)
        self.vBoxLayout.addWidget(self.qqLineEdit)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.activateCodeLabel)
        self.vBoxLayout.addSpacing(11)
        self.vBoxLayout.addWidget(self.activateCodeLineEdit)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.rememberCheckBox)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.loginButton)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.urlButton)
        self.vBoxLayout.addSpacing(30)
        self.vBoxLayout.addStretch(1)

    def __connectSignalToSlot(self):
        self.loginButton.clicked.connect(self._login)
        self.rememberCheckBox.stateChanged.connect(
            lambda: cfg.set(cfg.rememberMe, self.rememberCheckBox.isChecked())
        )

    def _login(self):
        logger.info("登录按钮被点击,登录事件触发")
        self.code = self.activateCodeLineEdit.text().strip()
        
        self.liscenseThread = LicenseServiceThread(self.qqLineEdit.text(), self.code)
        self.liscenseThread.resultSignal.connect(self._vaildateLogin)
        self.liscenseThread.finished.connect(lambda: self.liscenseThread.deleteLater())
        self.liscenseThread.start()
        logger.info("开始验证激活码")

    def _vaildateLogin(self, result):
        if not result:
            InfoBar.error(
                "激活失败",
                "请检查您的激活码",
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window(),
            )
            logger.error("激活码验证失败 原因: 无效的激活码")
        else:
            InfoBar.success(
                "激活成功",
                "恭喜您，激活成功！",
                position=InfoBarPosition.TOP,
                parent=self.window(),
            )
            logger.info("激活成功")

            if cfg.get(cfg.rememberMe):
                cfg.set(cfg.email, self.qqLineEdit.text().strip())
                cfg.set(cfg.activationCode, self.code)

            self.loginButton.setDisabled(True)
            QTimer.singleShot(1500, self._showMainWindow)

    def _showMainWindow(self):
        self.close()
        setThemeColor("#009faa")

        w = MainWindow()
        w.show()
        logger.info("登录成功,显示主窗口")
