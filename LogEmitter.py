import sys
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                             QVBoxLayout, QWidget, QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from datetime import datetime

'''
Descripttion: 
Author: Guo Guo
version: 
Date: 2025-08-22 14:03:06
LastEditors: Guo Guo
LastEditTime: 2025-08-22 14:03:17
'''
# 创建自定义信号类，用于线程安全的日志更新
class LogEmitter(QObject):
    log_signal = pyqtSignal(str)

    def write(self, text):
        self.log_signal.emit(str(text))
        