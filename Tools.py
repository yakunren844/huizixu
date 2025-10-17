from datetime import datetime
import json
import math
import os
import shutil
import threading
import time

import numpy as np
import pandas as pd
import requests
from SignalManager import signal_manager
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tqdm import tqdm

'''
Descripttion: 
Author: Guo Guo
version: 
Date: 2025-08-22 14:19:01
LastEditors: Guo Guo
LastEditTime: 2025-08-23 13:21:22
'''
class Tools:
    token_info={}
    login_url="https://api.likewon.com/api/Token/GetToken"
    upload_url="https://api.likewon.com/api/HZXModular/BatchAddMonitor"
    upload_file_number=0    #需要上传的文件数量
    failed_file_number=0    #上传失败的文件数量
    success_file_number=0    #上传成功的文件数量
    fixed_headers=['监测名单', '证件号码', '类型']
    def __init__(self):
        pass
        # self.username=username
        # self.password=password
        # self.upload_path=upload_path
        # self.service_id=service_id
        # self.whether=whether
        # self.day_max_number= day_max_number
        # self.last_time=last_time

    def init_upload(self,username,password,upload_path,service_id,whether, day_max_number,last_time):
        self.username=username
        self.password=password
        self.upload_path=upload_path
        self.service_id=service_id
        self.whether=whether
        self.day_max_number= day_max_number
        self.last_time=last_time

    def start_upload_thread(self):
        thread1 = threading.Thread(target=self.deal_files)
        thread1.start()
    
    def get_token(self):
        """获取token信息"""
        if "token" in self.token_info and "expires_in" in self.token_info:
            # print(datetime.now())
            cur_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(self.token_info["expires_in"])
            
            if cur_time < self.token_info["expires_in"]:
                return self.token_info
            else:
                self.token_info=self.login()
                return self.token_info
        else:
            self.token_info=self.login()
            return self.token_info
    
    def login(self):
        # 1. 准备要发送的JSON数据
        payload = {
            "user": self.username,
            "password": self.password,
            "typeStation": 1
            # 可以添加其他需要的参数
        }
        # 2. 设置请求头，指定内容类型为JSON
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            # 4. 发送POST请求
            response = requests.post(
                self.login_url,
                # data=json.dumps(payload),  # 将字典转换为JSON字符串
                json=payload,
                headers=headers
            )    
            # 5. 检查响应状态码
            if response.status_code == 200:
                # 6. 解析返回的JSON数据
                response_data = response.json()
                
                # 7. 打印返回的数据（可选）
                # print("API返回数据:")
                # print(json.dumps(response_data, indent=2, ensure_ascii=False))
                
                # 8. 检查返回的code是否为0（成功）
                if response_data.get("code") == 0:
                    # 9. 提取token信息
                    token_data = response_data.get("data", {})
                    token = token_data.get("token")
                    expires_in = token_data.get("expires_in")
                    token_type = token_data.get("token_type")
                    
                    print(f"\n获取Token成功:")
                    print(f"Token: {token}")
                    print(f"过期时间: {expires_in}")
                    print(f"Token类型: {token_type}")
                    
                    # 10. 准备要保存的数据
                    data_to_save = {
                        "token_info": token_data,
                        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "api_response": response_data
                    }
                    
                    # 11. 保存到JSON文件
                    # filename = f"./token/token_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    # with open(filename, "w", encoding="utf-8") as f:
                    #     json.dump(data_to_save, f, indent=2, ensure_ascii=False)
                    
                    # print(f"\n数据已保存到文件: {filename}")
                    return token_data
                else:
                    print(f"请求失败: {response_data.get('msg')}")
                    return None
            else:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求发生异常: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")
            print(f"响应内容: {response.text}")
            return None
   
    def process_data(self):
        # 发送开始处理的消息
        signal_manager.log_signal.emit("开始处理数据...")
        
        # 模拟数据处理
        for i in range(1, 101):
            # 发送进度消息（不换行）
            signal_manager.progress_signal.emit(100, i)
            time.sleep(0.1)
            
        # 发送完成消息
        signal_manager.log_signal.emit(" - 完成!")
        signal_manager.log_signal.emit("数据处理完成")

    def thread_split_excel(self,input_file, output_folder,deal_file_limit=10000):
        # 发送开始处理的消息
        signal_manager.log_signal.emit("开始处理数据...")
        # thread1 = threading.Thread(target=self.split_excel_pd,args=(input_file, output_folder,deal_file_limit))
        thread1 = threading.Thread(target=self.split_excel_merge,args=(input_file, output_folder,deal_file_limit))
        thread1.start()
        # thread1.join()
        # 发送完成消息
    def split_excel_pd2(self,input_file, output_folder,deal_file_limit=10000):
        """分割大Excel文件到临时文件夹"""
        signal_manager.btn_status_signal.emit(1,False)
        upload_file_list=[]
        upload_file_path=""
        
         # 读取 Excel 文件
        xls = pd.ExcelFile(input_file)
        all_dfs = []
        # 遍历每个 sheet
        for sheet_name in xls.sheet_names:
            # 读取 sheet 数据
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # 检查标题头
            if not all(header in df.columns for header in self.fixed_headers):
                signal_manager.log_signal.emit(f"Sheet '{sheet_name}' 缺少固定的标题头（监测名单、证件号码、类型），跳过")
                signal_manager.show_signal.emit(f"Sheet '{sheet_name}' 缺少固定的标题头（监测名单、证件号码、类型），跳过")
                break
            # 只保留固定的标题头列（忽略多余列）
            df = df[self.fixed_headers]
            # 如果 sheet 为空，仅保存标题头
            if df.empty:
                output_file = os.path.join(upload_file_path, 'excel', "part_0001.xlsx")
                df.to_excel(output_file, index=False, columns=self.fixed_headers)
                print(f"Sheet '{sheet_name}' 为空，生成文件: {output_file}")
                continue
            else:
                # 合并所有 DataFrame
                merged_df = pd.concat(all_dfs, ignore_index=True)
        
        # 1. 创建带时间戳的临时文件夹
        upload_file_path = os.path.join(output_folder, f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(upload_file_path, exist_ok=True)
        os.makedirs(f"{upload_file_path}/excel", exist_ok=True)
        os.makedirs(f"{upload_file_path}/failed", exist_ok=True)
        os.makedirs(f"{upload_file_path}/success", exist_ok=True)

        # print(f"创建文件夹: {upload_file_path}")
        try:
            # 读取 Excel 文件
            xls = pd.ExcelFile(input_file)
            # 遍历每个 sheet
            part_index=0
            for sheet_name in xls.sheet_names:
                # 读取 sheet 数据
                df = pd.read_excel(xls, sheet_name=sheet_name)

                # 检查标题头
                if not all(header in df.columns for header in self.fixed_headers):
                    signal_manager.log_signal.emit(f"Sheet '{sheet_name}' 缺少固定的标题头（监测名单、证件号码、类型），跳过")
                    signal_manager.show_signal.emit(f"Sheet '{sheet_name}' 缺少固定的标题头（监测名单、证件号码、类型），跳过")
                    break
                # 只保留固定的标题头列（忽略多余列）
                df = df[self.fixed_headers]
                # 如果 sheet 为空，仅保存标题头
                if df.empty:
                    output_file = os.path.join(upload_file_path, 'excel', "part_0001.xlsx")
                    df.to_excel(output_file, index=False, columns=self.fixed_headers)
                    print(f"Sheet '{sheet_name}' 为空，生成文件: {output_file}")
                    continue
                # 按 max_rows 分割数据
                total_rows = len(df)
                for start in range(0, total_rows, deal_file_limit):
                    # 提取当前分片
                    df_chunk = df.iloc[start:start + deal_file_limit]
                    # print(f"生成文件: {part_index}，行数: {len(df_chunk)}")
                    # 生成输出文件路径（part_0001, part_0002, ...）
                    # part_index =part_index+ start // deal_file_limit + 1
                    part_index =part_index + 1
                    # print(f"生成文件: {part_index}")
                    temp_name="part_"+str(part_index).zfill(3)+".xlsx"
                    output_file = os.path.join(upload_file_path,"excel",temp_name)

                    # 保存到新的 Excel 文件
                    df_chunk.to_excel(output_file, index=False, columns=self.fixed_headers)
                    upload_file_list.append(temp_name)
                    print(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
                    signal_manager.log_signal.emit(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
            signal_manager.trans_path_signal.emit(upload_file_path)
            signal_manager.log_signal.emit(f"分割大excel文件完成，保存目录: {upload_file_path}")
            signal_manager.btn_status_signal.emit(1,True)
            return upload_file_path

        except Exception as e:
            signal_manager.trans_path_signal.emit('')
            print(f"发生错误: {e}")
            signal_manager.btn_status_signal.emit(1,True)
            return None    
    def split_excel_merge(self,input_file, output_folder,deal_file_limit=10000):
        """
        先合并所有的sheet,然后再进行分割
        分割大Excel文件到临时文件夹"""
        signal_manager.btn_status_signal.emit(1,False)
        upload_file_list=[]
        upload_file_path=""
        
        
        # 1. 创建带时间戳的临时文件夹
        upload_file_path = os.path.join(output_folder, f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(upload_file_path, exist_ok=True)
        os.makedirs(f"{upload_file_path}/excel", exist_ok=True)
        os.makedirs(f"{upload_file_path}/failed", exist_ok=True)
        os.makedirs(f"{upload_file_path}/success", exist_ok=True)
        is_error=False
        # print(f"创建文件夹: {upload_file_path}")
        try:
            # 读取 Excel 文件
            xls = pd.ExcelFile(input_file)
            
            # 遍历每个 sheet
            part_index=0
            # 初始化一个空的DataFrame用于合并
            combined_df = pd.DataFrame()
            for sheet_name in xls.sheet_names:
                # 读取当前sheet的前三列
                df = pd.read_excel(xls, sheet_name=sheet_name,header=None)
                # 检查第一行第一列是否包含关键词
                if df.shape[0] > 0 and df.shape[1] > 0:
                    first_cell_value = str(df.iloc[0, 0]) if pd.notna(df.iloc[0, 0]) else ""
                    
                    if '名单' in first_cell_value or '名称' in first_cell_value or '列表' in first_cell_value:
                        # 丢弃第一行
                        df = df.iloc[1:].reset_index(drop=True)
                        print(f"Sheet '{sheet_name}': 丢弃了标题行")
                # 确保第三列存在
                # 检查列数并补足到三列
                current_cols = df.shape[1]
                # print(f"Sheet '{sheet_name}' 有 {current_cols} 列")
                if current_cols < 3:
                    # 需要补充的列数
                    cols_to_add = 3 - current_cols
                    # 添加新列
                    for i in range(cols_to_add):
                        new_col_name = f"c_{current_cols + i + 1}"
                        df[new_col_name] = ''
                        
                # 只保留前三列
                df = df.iloc[:, :3]
                df.columns = self.fixed_headers
               
                 # 根据第一列字符串长度修改第三列
                df['类型'] = df['监测名单'].apply(
                    lambda x: '个人' if isinstance(x, str) and len(str(x).strip()) < 5 else '企业'
                )
                    
                # 合并到总的DataFrame
                combined_df = pd.concat([combined_df, df], ignore_index=True)

            # combined_df.to_excel('combined_output.xlsx', index=False)
            # print('完成')
            # exit()

                
            # 按 max_rows 分割数据
            total_rows = len(combined_df)
            for start in range(0, total_rows, deal_file_limit):
                # 提取当前分片
                df_chunk = combined_df.iloc[start:start + deal_file_limit]

                # 生成输出文件路径（part_0001, part_0002, ...）
                # part_index = part_index + start // deal_file_limit + 1
                part_index = part_index  + 1
                temp_name="part_"+str(part_index).zfill(3)+".xlsx"
                output_file = os.path.join(upload_file_path,"excel",temp_name)

                # 保存到新的 Excel 文件
                df_chunk.to_excel(output_file, index=False, columns=self.fixed_headers)
                upload_file_list.append(temp_name)
                print(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
                signal_manager.log_signal.emit(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
            if is_error:
                signal_manager.btn_status_signal.emit(1,True)
                return None
            else:
                signal_manager.trans_path_signal.emit(upload_file_path)
                signal_manager.log_signal.emit(f"分割大excel文件完成，保存目录: {upload_file_path}")

            signal_manager.btn_status_signal.emit(1,True)
            print('处理完成！')
            return upload_file_path

        except Exception as e:
            signal_manager.trans_path_signal.emit('')
            print(f"发生错误: {e}")
            signal_manager.btn_status_signal.emit(1,True)
            return None
    def split_excel_pd(self,input_file, output_folder,deal_file_limit=10000):
        """分割大Excel文件到临时文件夹"""
        signal_manager.btn_status_signal.emit(1,False)
        upload_file_list=[]
        upload_file_path=""
        
        
        # 1. 创建带时间戳的临时文件夹
        upload_file_path = os.path.join(output_folder, f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(upload_file_path, exist_ok=True)
        os.makedirs(f"{upload_file_path}/excel", exist_ok=True)
        os.makedirs(f"{upload_file_path}/failed", exist_ok=True)
        os.makedirs(f"{upload_file_path}/success", exist_ok=True)
        is_error=False
        # print(f"创建文件夹: {upload_file_path}")
        try:
            # 读取 Excel 文件
            xls = pd.ExcelFile(input_file)
            # 遍历每个 sheet
            part_index=0
            for sheet_name in xls.sheet_names:
                # 读取 sheet 数据
                df = pd.read_excel(xls, sheet_name=sheet_name)

                # 检查标题头
                if not all(header in df.columns for header in self.fixed_headers):
                    signal_manager.log_signal.emit(f"Sheet '{sheet_name}' 缺少固定的标题头（监测名单、证件号码、类型），跳过")
                    signal_manager.show_signal.emit(f"Sheet '{sheet_name}' 缺少固定的标题头（监测名单、证件号码、类型），跳过")
                    is_error=True
                    try:
                        shutil.rmtree(upload_file_path)
                    except Exception as e:
                        print(f"移除目录失败：{e}")
                    break
                # 只保留固定的标题头列（忽略多余列）
                df = df[self.fixed_headers]
                # 如果 sheet 为空，仅保存标题头
                if df.empty:
                    output_file = os.path.join(upload_file_path, 'excel', "part_0001.xlsx")
                    df.to_excel(output_file, index=False, columns=self.fixed_headers)
                    print(f"Sheet '{sheet_name}' 为空，生成文件: {output_file}")
                    continue
                # 按 max_rows 分割数据
                total_rows = len(df)
                for start in range(0, total_rows, deal_file_limit):
                    # 提取当前分片
                    df_chunk = df.iloc[start:start + deal_file_limit]

                    # 生成输出文件路径（part_0001, part_0002, ...）
                    # part_index = part_index + start // deal_file_limit + 1
                    part_index = part_index  + 1
                    temp_name="part_"+str(part_index).zfill(3)+".xlsx"
                    output_file = os.path.join(upload_file_path,"excel",temp_name)

                    # 保存到新的 Excel 文件
                    df_chunk.to_excel(output_file, index=False, columns=self.fixed_headers)
                    upload_file_list.append(temp_name)
                    print(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
                    signal_manager.log_signal.emit(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
            if is_error:
                signal_manager.btn_status_signal.emit(1,True)
                return None
            else:
                signal_manager.trans_path_signal.emit(upload_file_path)
                signal_manager.log_signal.emit(f"分割大excel文件完成，保存目录: {upload_file_path}")

            signal_manager.btn_status_signal.emit(1,True)
            return upload_file_path

        except Exception as e:
            signal_manager.trans_path_signal.emit('')
            print(f"发生错误: {e}")
            signal_manager.btn_status_signal.emit(1,True)
            return None
    def upload_excel(self,file_path):
        """根据文件扩展名返回对应的Excel MIME类型"""
        ext = os.path.splitext(file_path)[1].lower()
        token=self.get_token()
        if token is None:
            print("登录失败，请检查账户和密码！")
            raise Exception
        
        mime_map = {
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xlsm': 'application/vnd.ms-excel.sheet.macroEnabled.12',
            '.xltx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
            '.xlsb': 'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
            '.xls': 'application/vnd.ms-excel',
        }
        
        # 返回对应的MIME类型，如果找不到则默认使用.xlsx的类型
        mime_type = mime_map.get(ext, mime_map['.xlsx'])
        # print("文件类型:", mime_type)
        try:

            with open(file_path, 'rb') as f:
                file_content = f.read()
                multipart_data = MultipartEncoder(
                    fields={
                        'ServiceId': str(self.service_id),
                        'Whether': str(self.whether),
                        'DayMaxNumber': str(self.day_max_number),
                        'LastTime': self.last_time,
                        'files': (os.path.basename(file_path), file_content, mime_type)
                    }
                )
                # 准备请求头，包含Authorization
                headers = {
                        'Accept': 'application/json',
                        'Content-Type': multipart_data.content_type,  # 这里设置正确的content-type和boundary
                        'Authorization': f'Bearer {token["token"]}'
                        }
                response = requests.post(self.upload_url,data=multipart_data, headers=headers,timeout=600)
                if response.status_code == 200:
                    ret_json=response.json()
                    if ret_json['code'] == 0:
                        print("文件上传成功！")
                        return True
                    else:
                        print("文件上传失败！", ret_json['msg'])
                        signal_manager.log_signal.emit(f"文件上传失败！{ret_json['msg']}")
                        return False
                else:
                    print("文件上传失败！",response.text)
                    return False
        except Exception as e:
            print("文件上传失败！", e)
            return False
    def pre_upload_path(self):
        '''
        处理文件夹
        '''
        deal_file_path=self.upload_path
        if deal_file_path=="":
            print("处理文件夹，deal_file_path文件路径不能为空")
            exit()

        excel_file_path=os.path.join(deal_file_path, "excel")
        if not os.path.exists(excel_file_path):
            os.makedirs(excel_file_path)
            print("处理文件夹，excel文件夹不存在,创建excel文件夹")
        success_file_path=os.path.join(deal_file_path, "success")
        if not os.path.exists(success_file_path):
            os.makedirs(success_file_path)
            print("处理文件夹，success文件夹不存在，创建success文件夹")

        failed_file_path=os.path.join(deal_file_path, "failed")
        if not os.path.exists(failed_file_path):
            os.makedirs(failed_file_path)
            print("处理文件夹，failed文件夹不存在，创建failed文件夹")

        for file in os.listdir(deal_file_path):
            if file.endswith(".xlsx") or file.endswith(".xls"):
                shutil.move(os.path.join(deal_file_path, file), os.path.join(excel_file_path, file))
        file_path=deal_file_path

        return file_path
    
    def get_excel_number(self):
        excel_file_path=os.path.join(self.upload_path, "excel")
        file_number=0
        for file in os.listdir(excel_file_path):
            if file.endswith(".xlsx") or file.endswith(".xls"):
                file_number+=1
        self.upload_file_number=file_number
        return file_number
    
    def deal_files(self):
        upload_file_number=self.get_excel_number()    #需要上传的文件数量
        failed_file_number=0    #上传失败的文件数量
        success_file_number=0    #上传成功的文件数量


        excel_file_path=os.path.join(self.upload_path, "excel")
        for file in os.listdir(excel_file_path):
            if file.endswith(".xlsx") or file.endswith(".xls"):
                cur_path=os.path.join(self.upload_path, "excel", file)
                file_success_path=os.path.join(self.upload_path, "success", file)
                file_failed_path=os.path.join(self.upload_path, "failed", file)
                ret=self.upload_excel(cur_path)
                if ret:
                    success_file_number+=1
                    shutil.move(cur_path, file_success_path)
                    signal_manager.progress_signal.emit(upload_file_number, success_file_number, failed_file_number)
                    print(f"{file}文件上传成功！")
                    signal_manager.log_signal.emit(f"{file}文件上传成功！")
                else:
                    shutil.move(cur_path, file_failed_path)
                    failed_file_number+=1
                    signal_manager.progress_signal.emit(upload_file_number, success_file_number, failed_file_number)
                    signal_manager.log_signal.emit(f"{file}文件上传失败！")
                    print(f"{file}文件上传失败！")
        signal_manager.btn_status_signal.emit(2,True)
        signal_manager.log_signal.emit("处理完成")
        signal_manager.show_signal.emit("处理完成")
        print(f"需要上传的文件数量：{upload_file_number}",f",上传成功：{success_file_number}",f",上传失败：{failed_file_number}")    

    def merge_excel_excels(self,folder_path, output_path):
        """
        将所有Excel文件中的所有Sheet合并到一个Sheet中
        """
        
        # 获取所有Excel文件
        excel_files = [f for f in os.listdir(folder_path) 
                    if f.endswith(('.xlsx', '.xls'))]
        
        combined_df = pd.DataFrame() 
        
        print(f"找到 {len(excel_files)} 个Excel文件")
        
        for file in tqdm(excel_files, desc="处理文件中"):
            file_path = os.path.join(folder_path, file)
            
            try:
                # 读取Excel文件的所有Sheet
                excel_file = pd.ExcelFile(file_path)
                
                for sheet_name in excel_file.sheet_names:
                    # 读取每个Sheet
                    print(f"处理文件 {file}, Sheet {sheet_name}")
                    df = pd.read_excel(file_path, 
                                        sheet_name=sheet_name,
                                        header=None,  # 关键参数：无标题行
                                        dtype=str)     # 统一读为字符串，避免类型问题)
                    
                    # 检查第一行第一列是否包含关键词
                    if df.shape[0] > 0 and df.shape[1] > 0:
                        first_cell_value = str(df.iloc[0, 0]) if pd.notna(df.iloc[0, 0]) else ""
                        
                        if '名单' in first_cell_value or '名称' in first_cell_value or '列表' in first_cell_value:
                            # 丢弃第一行
                            df = df.iloc[1:].reset_index(drop=True)
                            print(f"Sheet '{sheet_name}': 丢弃了标题行")
                    # 确保第三列存在
                    # 检查列数并补足到三列
                    current_cols = df.shape[1]
                    # print(f"Sheet '{sheet_name}' 有 {current_cols} 列")
                    if current_cols < 3:
                        # 需要补充的列数
                        cols_to_add = 3 - current_cols
                        # 添加新列
                        for i in range(cols_to_add):
                            new_col_name = f"c_{current_cols + i + 1}"
                            df[new_col_name] = ''
                            
                    # 只保留前三列
                    df = df.iloc[:, :3]
                    df.columns = self.fixed_headers
                
                    # 根据第一列字符串长度修改第三列
                    df['类型'] = df['监测名单'].apply(
                        lambda x: '个人' if isinstance(x, str) and len(str(x).strip()) < 5 else '企业'
                    )
                        
                    # 合并到总的DataFrame
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                        
            except Exception as e:
                print(f"处理文件 {file} 时出错: {e}")
                continue
        
        # 如果有数据，保存到新的Excel文件
        if not combined_df.empty:
            merged_df = combined_df.drop_duplicates()
            # merged_df.to_excel(output_file, index=False)
            self.split_pd_excel(merged_df,output_path)
            print(f"合并后的数据已保存到 {output_path}")
            
        else:
            print("没有找到有效数据")
            return None
    
    def split_pd_excel(self,combined_df, output_path,deal_file_limit=10000):
            os.makedirs(output_path, exist_ok=True)
            os.makedirs(f"{output_path}/excel", exist_ok=True)
            os.makedirs(f"{output_path}/failed", exist_ok=True)
            os.makedirs(f"{output_path}/success", exist_ok=True)
            # 按 max_rows 分割数据
            total_rows = len(combined_df)
            part_index = 0
            for start in range(0, total_rows, deal_file_limit):
                # 提取当前分片
                df_chunk = combined_df.iloc[start:start + deal_file_limit]

                # 生成输出文件路径（part_0001, part_0002, ...）
                # part_index = part_index + start // deal_file_limit + 1
                part_index = part_index  + 1
                temp_name="part_"+str(part_index).zfill(3)+".xlsx"
                output_file = os.path.join(output_path,"excel",temp_name)

                # 保存到新的 Excel 文件
                df_chunk.to_excel(output_file, index=False, columns=self.fixed_headers)
                print(f"生成文件: {temp_name}，行数: {len(df_chunk)}")
                
            

# 使用示例
# split_to_multiple_sheets(merged_df, "large_data_multi_sheet.xlsx")
if __name__ == "__main__":
    t=Tools()
    t.merge_excel_excels("C:\\Users\\Administrator\\Desktop\\浙江_江苏",  "zhejiang_jiangsu")
    
