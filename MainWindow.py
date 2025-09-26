'''
Descripttion: 
Author: Guo Guo
version: 
Date: 2025-08-22 14:10:05
LastEditors: Guo Guo
LastEditTime: 2025-08-25 09:19:54
'''
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
from SignalManager import signal_manager
from Tools import Tools
# 创建自定义信号类，用于线程安全的日志更新
class LogEmitter(QObject):
    log_signal = pyqtSignal(str)

    def write(self, text):
        self.log_signal.emit(str(text))
# 主窗口类
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('huizix.ui', self)
         # 设置统一字体
        app_font = QFont("Arial", 10)  # 使用跨平台字体
        QApplication.setFont(app_font)

        self.setFixedSize(self.width(), self.height())
        self.setup_logging()
        # 设置窗口图标
        self.setWindowIcon(QIcon('app.ico'))
        # 连接信号
        signal_manager.log_signal.connect(self.log_msg)
        signal_manager.progress_signal.connect(self.update_progress)
    
        signal_manager.show_signal.connect(self.show_msgbox)
        signal_manager.trans_path_signal.connect(self.get_save_path)
        signal_manager.btn_status_signal.connect(self.set_btn_status)
        # 设置进度条
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        
        self.selectXinhao.addItem("m10/普通精准", 209733)
        self.selectXinhao.addItem("m60/普通精准", 212888)
        self.selectXinhao.addItem("D/普通精准", 209734)
        self.selectXinhao.setCurrentIndex(0)
    
        # 连接按钮点击事件
        self.selectExcelFile.clicked.connect(self.select_excel_file)
        self.selectSavePath.clicked.connect(self.select_save_folder)
        self.selectUploadPath.clicked.connect(self.select_upload_folder)
        self.startUpload.clicked.connect(self.start_upload)
        self.startSplitExcel.clicked.connect(self.start_split_excel)
        self.savePath.setText(os.getcwd())

        # 获取当前日期
        current_date = QDate.currentDate()
        
        # 计算半年后的日期（当前日期 + 6个月）
        half_year_later = current_date.addMonths(6)
        
        # 设置 QDateEdit 的日期为半年后
        self.dateLimit.setDate(half_year_later)
    
    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        try:
            signal_manager.log_signal.disconnect(self.log_msg)
            signal_manager.progress_signal.disconnect(self.update_progress)
            signal_manager.show_signal.disconnect(self.show_msgbox)
            signal_manager.trans_path_signal.disconnect(self.get_save_path)
            signal_manager.btn_status_signal.disconnect(self.set_btn_status)
            self.log_emitter.log_signal.disconnect(self.append_log)
            self.log_emitter._connected = False
        except Exception as e:
            # self.error_signal.emit(f"处理错误: {str(e)}")
            pass
        # self.log_emitter.destroyed()

    def set_btn_status(self,btn,flag):
        if btn==1:
            self.startSplitExcel.setEnabled(flag)
        elif btn==2:
            self.startUpload.setEnabled(flag)
            
    def start_split_excel(self):
        tt=Tools()
        if self.excelFile.text().strip()=="":
            self.show_msgbox("请选择Excel文件")
            return
        file_name=os.path.basename(self.excelFile.text())
        print(file_name)
        limit_num=int(self.limitCount.text())
        if limit_num<100:
            limit_num=5000
            self.show_msgbox("分割参数不正确，分割值太低.区间：1000-5000")
            self.limitCount.setText("5000")
            return
        ret=tt.thread_split_excel(self.excelFile.text(),self.savePath.text(),limit_num)
        self.startSplitExcel.setEnabled(False)
        # if ret:
        #     self.uploadPath.setText(ret)
        #     self.show_msgbox("分割完成")

    def show_msgbox(self,msg):
        QMessageBox.information(self, "提示", msg)

    def get_save_path(self,path):
        if path:
            self.uploadPath.setText(path)

    def start_upload(self):
        upload_path=self.uploadPath.text().strip()
        account=self.account.text().strip()
        password=self.password.text().strip()
        day_max_number=int(self.perDayLimit.text().strip())
        last_time=self.dateLimit.date().toString(Qt.ISODate)
        service_id=self.selectXinhao.currentData()
        whether=2   #暂时不知道是什么
        self.progressBar.setValue(0)
        
        if upload_path=="":
            self.show_msgbox("请选择上传文件所在目录,不用包含excel目录")
            return
        if account=="":
            self.show_msgbox("请输入上传账号")
            return
        if password=="":
            self.show_msgbox("请输入上传密码")
            return
        if day_max_number<1:
            self.show_msgbox("每日限制不正确，必须大于0的整数")
            return
        
        current_date = QDate.currentDate()
        # 计算半年后的日期（当前日期 + 6个月）
        one_year_later = current_date.addMonths(12)
        if last_time>one_year_later.toString(Qt.ISODate) or last_time<current_date.toString(Qt.ISODate):
            self.show_msgbox("上传时间不正确，时间间隔不能超过1年切大于当前时间")
            return
                
        tt=Tools()
        tt.init_upload(account,password,upload_path,service_id,whether, day_max_number,last_time)
        tt.pre_upload_path()
        self.startUpload.setEnabled(False)
        tt.start_upload_thread()
        

    def update_progress(self, tolal_num,success_num,failed_num):
        progress = int(((success_num+failed_num) / tolal_num) * 100)
        self.progressBar.setValue(progress)
        self.progressLabel.setText(f"进度:{progress}%，成功:{success_num}，失败：{failed_num}")
    

    def select_upload_folder(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(
            self,  # 父窗口
            "选择文件夹",  # 对话框标题
            "",  # 默认打开的路径（空字符串表示当前目录）
            QFileDialog.ShowDirsOnly  # 只显示文件夹
        )
        
        # 检查是否选择了文件夹
        if folder_path:
            self.uploadPath.setText(folder_path)
            self.statusBar().showMessage(f"选择上传文件所在目录: {folder_path}")
            self.logger.debug(f"上传文件所在目录: {folder_path}")
            
        else:
            self.statusBar().showMessage("未选择保存文件目录，如果为空，默认保存至当前目录")
    
    def select_save_folder(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(
            self,  # 父窗口
            "选择文件夹",  # 对话框标题
            "",  # 默认打开的路径（空字符串表示当前目录）
            QFileDialog.ShowDirsOnly  # 只显示文件夹
        )
        
        # 检查是否选择了文件夹
        if folder_path:
            self.savePath.setText(folder_path)
            self.statusBar().showMessage(f"保存分割文件目录: {folder_path}")
            self.logger.debug(f"保存分割文件目录: {folder_path}")
            
        else:
            self.statusBar().showMessage("未选择保存文件目录，如果为空，默认保存至当前目录")
            

    def select_excel_file(self):
        # 打开文件选择对话框，只显示Excel文件
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            '选择 Excel 文件', 
            '',  # 初始目录为空，使用系统默认
            'Excel 文件 (*.xlsx *.xls);;所有文件 (*)'
        )
        
        # 如果用户选择了文件（没有点击取消）
        if file_path:
            self.file_path = file_path
            self.excelFile.setText(file_path)
            
            # # 启用操作按钮
            # self.view_button.setEnabled(True)
            # self.process_button.setEnabled(True)
            
            # 更新状态栏
            file_name = os.path.basename(file_path)
            self.logger.debug(f'已选择文件: {file_name}')
            self.statusBar().showMessage(f'已选择文件: {file_name}')
    def setup_logging(self):
        # 创建日志发射器
        self.log_emitter = LogEmitter()
        self.log_emitter.log_signal.connect(self.append_log)
        
        # 配置日志记录器
        self.logger = logging.getLogger('AppLogger')
        self.logger.setLevel(logging.DEBUG)
        
        # 创建自定义处理器，将日志重定向到界面
        handler = logging.StreamHandler(self.log_emitter)
        handler.setLevel(logging.DEBUG)
        
        # 设置日志格式
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        self.logger.addHandler(handler)
    def log_msg(self,msg):
        self.logger.debug(msg)

    def append_log(self, text,newline=True):
        # 在文本末尾添加新日志
        self.logShow.moveCursor(self.logShow.textCursor().End)
        self.logShow.insertPlainText(text)
        
        # 自动滚动到底部
        scrollbar = self.logShow.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clear_log(self):
        self.logShow.clear()

if __name__ == '__main__':
     # 创建应用前禁用logging shutdown
    logging.shutdown = lambda: None
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    