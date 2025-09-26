import os
import shutil
import requests
import json
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder

username="18680676627"
password="123456"

login_url="https://api.likewon.com/api/Token/GetToken"
upload_url="https://api.likewon.com/api/HZXModular/BatchAddMonitor"
token_info={}
ServiceId=209733        #m10/普通精准
Whether=2               #暂时不知道是什么
LastTime='2026-03-20'   #到期日期
DayMaxNumber=10000         #每日最大数量

def get_token():
    """获取token信息"""
    global token_info
    if "token" in token_info and "expires_in" in token_info:
        print(datetime.now())
        cur_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(datetime.strptime(token_info["expires_in"], "%Y-%m-%d %H:%M:%S"))
        
        if cur_time < datetime.strptime(token_info["expires_in"], "%Y-%m-%d %H:%M:%S"):
            return token_info
        else:
            token_info=login()
            return token_info
    else:
        token_info=login()
        return token_info
    
def login():
    # 1. 准备要发送的JSON数据
    payload = {
        "user": username,
        "password": password,
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
            login_url,
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
                filename = f"./token/token_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, indent=2, ensure_ascii=False)
                
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
def upload_excel(file_path):
    """根据文件扩展名返回对应的Excel MIME类型"""
    ext = os.path.splitext(file_path)[1].lower()
    token=get_token()
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
                    'ServiceId': str(ServiceId),
                    'Whether': str(Whether),
                    'DayMaxNumber': str(DayMaxNumber),
                    'LastTime': LastTime,
                    'files': (os.path.basename(file_path), file_content, mime_type)
                }
            )
            # 准备请求头，包含Authorization
            headers = {
                    'Accept': 'application/json',
                    'Content-Type': multipart_data.content_type,  # 这里设置正确的content-type和boundary
                    'Authorization': f'Bearer {token['token']}'
                    }
            response = requests.post(upload_url,data=multipart_data, headers=headers,timeout=600)
            
            if response.status_code == 200:
                ret_json=response.json()
                if ret_json['code'] == 0:
                    print("文件上传成功！")
                    return True
                else:
                    print("文件上传失败！", ret_json['msg'])
                    return False
            else:
                print("文件上传失败！",response.text)
                return False
    except Exception as e:
        print("文件上传失败！", e)
        return False
    
def deal_files(base_path):
    upload_file_number=0    #需要上传的文件数量
    failed_file_number=0    #上传失败的文件数量
    success_file_number=0    #上传成功的文件数量

    excel_file_path=os.path.join(base_path, "excel")
    for file in os.listdir(excel_file_path):
        if file.endswith(".xlsx"):
            
            cur_path=os.path.join(base_path, "excel", file)
            file_success_path=os.path.join(base_path, "success", file)
            file_failed_path=os.path.join(base_path, "failed", file)
            upload_file_number+=1
            ret=upload_excel(cur_path)
            if ret:
                success_file_number+=1
                shutil.move(cur_path, file_success_path)
                print(f"{file}文件上传成功！")
            else:
                shutil.move(cur_path, file_failed_path)
                failed_file_number+=1
                print(f"{file}文件上传失败！")
    print(f"需要上传的文件数量：{upload_file_number}",f",上传成功：{success_file_number}",f",上传失败：{failed_file_number}")    

# 调用函数
if __name__ == "__main__":
    deal_files("D:\\develop\\huizixu\\output_ok")
    # result = get_token()
    # print(result)
    # if result:
    #     print("\n操作成功完成！")
    # else:
    #     print("\n登录失败！")