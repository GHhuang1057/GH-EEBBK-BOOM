# coding:utf-8
import os
import sys
from datetime import datetime
from loguru import logger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from app.common.config import cfg
from app.view.register_window import RegisterWindow


# 启用dpi比例
if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))
else:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

currentTime = datetime.now()
currentDate = datetime.now().date()
logger.add(f"logs/eeebk_boom.log")
logger.info(f"软件于{currentTime}启动,若出现报错请从最新的该消息处开始复制")

# 创建应用程序
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
logger.info(f"创建主程序")
# 创建主窗口
w = RegisterWindow()
w.show()
logger.info(f"创建注册窗口")

app.exec()
