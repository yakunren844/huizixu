import datetime
import os
import sys
import logging
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
                             QFileDialog, QMessageBox, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
class GenjinAppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GenjinAppWindow, self).__init__()
        uic.loadUi('genjin.ui', self)
         # 设置统一字体
        app_font = QFont("Arial", 10)  # 使用跨平台字体
        QApplication.setFont(app_font)

        self.setFixedSize(self.width(), self.height())
        
        # 设置窗口图标
        self.setWindowIcon(QIcon('app.ico'))
        # 设置每列的最小宽度
        self.tableWidget.setColumnWidth(0, max(80, self.tableWidget.columnWidth(0)))
        self.tableWidget.setColumnWidth(1, max(300, self.tableWidget.columnWidth(1)))
        self.tableWidget.setColumnWidth(2, max(50, self.tableWidget.columnWidth(2)))
        self.tableWidget.setColumnWidth(3, max(80, self.tableWidget.columnWidth(3)))
        

if __name__ == '__main__':
     # 创建应用前禁用logging shutdown
    
    app = QtWidgets.QApplication(sys.argv)
    window = GenjinAppWindow()
    window.show()
    sys.exit(app.exec_())
