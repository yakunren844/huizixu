import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkcalendar import DateEntry  # 使用DateEntry组件
import pandas as pd
import os
import threading
import time
from datetime import datetime
import re

class EnhancedExcelProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel处理工具 - 专业版")
        self.root.geometry("700x650")
        
        # 设置样式
        self.root.configure(bg="#f0f0f0")
        font_style = ("Arial", 10)
        
        # 创建主框架
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # 1. Excel文件选择部分
        file_frame = tk.LabelFrame(main_frame, text="选择Excel文件", bg="#f0f0f0", font=font_style)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_path = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.file_path, width=50, state='readonly').pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="浏览...", command=self.browse_file, bg="#e1e1e1").pack(side=tk.LEFT, padx=5)
        
        # 2. 用户认证部分
        auth_frame = tk.LabelFrame(main_frame, text="用户认证", bg="#f0f0f0", font=font_style)
        auth_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(auth_frame, text="用户名:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.username_entry = tk.Entry(auth_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(auth_frame, text="密码:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = tk.Entry(auth_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 3. 日期输入部分（可手动输入也可选择）
        date_frame = tk.LabelFrame(main_frame, text="选择日期", bg="#f0f0f0", font=font_style)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 使用DateEntry组件，支持手动输入和日历选择
        tk.Label(date_frame, text="日期:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.date_entry = DateEntry(
            date_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            font=("Arial", 10))
        self.date_entry.pack(side=tk.LEFT, padx=5)
        
        # 添加日期格式验证
        self.date_entry.bind("<FocusOut>", self.validate_date)
        
        # 4. 数量输入部分
        quantity_frame = tk.LabelFrame(main_frame, text="输入数量", bg="#f0f0f0", font=font_style)
        quantity_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(quantity_frame, text="数量:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.quantity_entry = tk.Entry(quantity_frame, width=10, validate="key")
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(quantity_frame, text="(请输入正整数)", bg="#f0f0f0").pack(side=tk.LEFT)
        
        # 设置数量输入验证（只允许数字）
        self.quantity_entry['validatecommand'] = (self.quantity_entry.register(self.validate_number), '%P')
        
        # 5. 日志框
        log_frame = tk.LabelFrame(main_frame, text="处理日志", bg="#f0f0f0", font=font_style)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            width=80, 
            height=18, 
            wrap=tk.WORD, 
            bg="white", 
            fg="black",
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 6. 开始按钮和状态栏
        bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.start_button = tk.Button(
            bottom_frame, 
            text="开始处理", 
            command=self.start_processing, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"),
            width=15
        )
        self.start_button.pack(side=tk.LEFT, pady=5)
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        tk.Label(bottom_frame, textvariable=self.status_var, bg="#f0f0f0", fg="blue").pack(side=tk.RIGHT, padx=10)
        
        # 绑定输入检查事件
        self.file_path.trace_add("write", self.check_inputs)
        self.username_entry.bind("<KeyRelease>", lambda e: self.check_inputs())
        self.password_entry.bind("<KeyRelease>", lambda e: self.check_inputs())
        self.quantity_entry.bind("<KeyRelease>", lambda e: self.check_inputs())
        self.date_entry.bind("<<DateEntrySelected>>", lambda e: self.check_inputs())
        
        # 初始禁用开始按钮
        self.check_inputs()
    
    def browse_file(self):
        """浏览并选择Excel文件"""
        filetypes = [
            ("Excel文件", "*.xlsx *.xls"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=filetypes
        )
        
        if filename:
            self.file_path.set(filename)
            self.log_message(f"已选择文件: {filename}")
            self.status_var.set(f"已选择文件: {os.path.basename(filename)}")
    
    def validate_date(self, event=None):
        """验证日期格式"""
        date_str = self.date_entry.get()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            self.status_var.set("日期格式正确")
            return True
        except ValueError:
            self.status_var.set("错误: 日期格式应为YYYY-MM-DD")
            messagebox.showerror("错误", "日期格式不正确，请输入YYYY-MM-DD格式的日期")
            self.date_entry.focus_set()
            return False
    
    def validate_number(self, new_value):
        """验证数量输入是否为数字"""
        if new_value == "" or new_value.isdigit():
            return True
        else:
            self.bell()  # 发出警告声
            return False
    
    def check_inputs(self, *args):
        """检查所有必填项是否完成"""
        has_file = bool(self.file_path.get())
        has_username = bool(self.username_entry.get())
        has_password = bool(self.password_entry.get())
        has_quantity = bool(self.quantity_entry.get())
        has_valid_date = self.validate_date()
        
        if has_file and has_username and has_password and has_quantity and has_valid_date:
            self.start_button.config(state=tk.NORMAL)
            self.status_var.set("就绪 - 可以开始处理")
        else:
            self.start_button.config(state=tk.DISABLED)
            self.status_var.set("请完成所有必填字段")
    
    def log_message(self, message):
        """向日志框添加消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_processing(self):
        """开始处理Excel文件"""
        # 获取所有输入值
        filepath = self.file_path.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        date = self.date_entry.get()
        
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("错误", "数量必须大于0！")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的正整数数量！")
            return
        
        # 验证输入
        if not os.path.exists(filepath):
            messagebox.showerror("错误", "文件不存在！")
            return
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码！")
            return
        
        if not self.validate_date():
            return
        
        # 禁用按钮防止重复点击
        self.start_button.config(state=tk.DISABLED)
        self.status_var.set("处理中...")
        
        self.log_message("\n=== 开始处理 ===")
        self.log_message(f"用户名: {username}")
        self.log_message(f"文件: {filepath}")
        self.log_message(f"日期: {date}")
        self.log_message(f"数量: {quantity}")
        
        # 在后台线程中处理Excel
        processing_thread = threading.Thread(
            target=self.process_excel,
            args=(filepath, username, password, date, quantity),
            daemon=True
        )
        processing_thread.start()
    
    def process_excel(self, filepath, username, password, date, quantity):
        """模拟处理Excel文件的过程"""
        try:
            # 模拟读取Excel
            self.log_message("\n读取Excel文件...")
            time.sleep(1)
            
            # 这里可以添加实际的Excel处理代码
            # 例如: df = pd.read_excel(filepath)
            
            # 模拟处理过程
            self.log_message("验证用户权限...")
            time.sleep(0.5)
            
            self.log_message("处理数据...")
            for i in range(1, 6):
                time.sleep(0.5)
                progress = i*20
                self.log_message(f"处理进度: {progress}%")
                self.root.after(0, lambda: self.status_var.set(f"处理中... {progress}%"))
            
            self.log_message("数据校验...")
            time.sleep(1)
            
            self.log_message("=== 处理完成 ===")
            self.log_message(f"共处理了 {quantity} 条记录")
            self.log_message(f"处理日期: {date}")
            
            self.root.after(0, lambda: self.status_var.set("处理完成"))
            
        except Exception as e:
            self.log_message(f"错误: {str(e)}")
            self.root.after(0, lambda: self.status_var.set(f"错误: {str(e)}"))
        finally:
            # 重新启用开始按钮
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedExcelProcessorApp(root)
    root.mainloop()