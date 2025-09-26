'''
Descripttion: 
Author: Guo Guo
version: 
Date: 2025-08-22 16:45:55
LastEditors: Guo Guo
LastEditTime: 2025-08-23 16:16:42
'''
from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):
    # 日志信号
    log_signal = pyqtSignal(str)
    
    # 进度信号
    progress_signal = pyqtSignal(int,int,int)
    
    # 状态信号
    status_signal = pyqtSignal(str)

    # 状态信号
    show_signal = pyqtSignal(str)
    
    # 文件加载信号
    file_loaded_signal = pyqtSignal(str)

    trans_path_signal=pyqtSignal(str)
    btn_status_signal=pyqtSignal(int,bool)

# 创建全局信号管理器实例
signal_manager = SignalManager()