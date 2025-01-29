# coding: utf-8
from pathlib import Path

# change DEBUG to False if you want to compile the code to exe
DEBUG = "__compiled__" not in globals()


YEAR = 2025
AUTHOR = "GH工作室"
VERSION = "v0.0.1"
APP_NAME = "EEBBK BOOM"
CONFIG_FOLDER = Path('config').absolute()
CONFIG_FILE = CONFIG_FOLDER / "config.json"
