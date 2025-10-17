
from datetime import datetime
import requests
from fastapi import FastAPI
from datetime import datetime
import uvicorn
import urllib3
import ssl
# 禁用 SSL 警告
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings()

# # 创建会话
# session = requests.Session()

# # 针对 Python 3.12 的 SSL 配置
# session.verify = False  # 禁用 SSL 验证

class Daka:
    CompanyId="461"
    login_url="https://api1.likewon.cn/api/Token"
    daka_url="https://timeapi.lawxp.com/api/Card/AddCardLog"
    daka_get_url="https://timeapi.lawxp.com/api/Card/AddCardLogBad"
    get_url="https://timeapi.lawxp.com/api/App_My/GetPersonalData?companyId=461&userId=2103470328"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "trust/5.0.294 (iPhone; iOS 18.6; Scale/3.00)",
        
        # "Authorization":f"Bearer {token}"
    }
    def get_json_token(self,url,params=None):
        token=self.user_info['accessToken']
        get_header=self.headers.copy() 
        get_header['Authorization'] = f'Bearer {token}'
        res=requests.get(url,params=params,headers=get_header)
        if res.status_code==200 and res.json()['code']==0:
            return res.json()
        else:
            return None
        
    def post_form_data(self,url,data):
        token=self.user_info['accessToken']
        get_header=self.headers.copy() 
        get_header['Authorization'] = f'Bearer {token}'
        get_header["Content-Type"]="application/x-www-form-urlencoded"
        res=requests.post(url,data=data,headers=get_header,timeout=10,verify=False)
        if res.status_code==200 and res.json()['code']==0:
            return res.json()
        else:
            return None
    def daka_post(self):
        CardTime=datetime.now().strftime('%H:%M:%S')

        form_data={
            "ApprovalId":"",
            "ApprovalInfoId":"",
            "AttenceGroupId":"222",
            "AttendanceTime":"18:00",
            "CardAddress":"广东省广州市番禺区兴南大道靠近诺德天街",
            "CardEquipment":"iPhone XS",
            "CardResult":"",
            "CardTime":CardTime,
            "CardType":"0",
            "CompanyId":self.CompanyId,
            "File":"",
            "File2Id":"0",
            "FileId":"0",
            "IsAutomation":"false",
            "IsSameAddr":"true",
            "RelationId":"125",
            "Remark":"",
            "ShiftId":"181",
            "ShiftTimeId":"236",
            "ShiftTimeType":"2",
            "UserId":self.user_info['wwwUserId'],
            "WorkOrderId":"0",
            "lat":"23.009195",
            "lng":"113.351668"
        }	
        res=self.post_form_data(self.daka_url,form_data)
        print(res)
        return res
        
    def daka_get(self):
        CardTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data={
            "UserId":self.user_info['wwwUserId'],
            "CompanyId":self.CompanyId,
            "AttenceTime":"08:50-18:00",
            "CardAddress":"广东省广州市番禺区兴南大道靠近诺德天街",
            "CardEquipment":"iPhone XS",
            "CardTime":CardTime,
            "IsAutomation":"false",
            "Lat":"23.009209",
            "Lng":"113.351663",
            "type":0
            }
        res=self.get_json_token(self.daka_get_url,data)
        print(res)
        
    def login(self,username,password):
        json_data={
            "account": username,
            "password": password,
            "type": 3
            }
        res=requests.post(self.login_url,json=json_data,timeout=10,verify=False)
        print(res.json())
        print(res.status_code)

        if int(res.status_code)==200 and int(res.json()['code'])==0:
            self.user_info=res.json()['data']
        else:
            self.user_info=None
        

    def __init__(self):
        pass
# app = FastAPI(title="My API", version="1.0.0")
# # 根路径 GET 接口
# @app.get("/daka")
# async def root():
#     daka=Daka()
#     login_res=daka.login("guojiancheng","Gjc523220313")
#     print(login_res)
#     res=daka.daka_post()
#     print(res)
#     return res
if __name__ == '__main__':
#     # uvicorn.run(app, host="0.0.0.0", port=9108)
    daka=Daka()
    daka.login("guojiancheng","Gjc523220313")
    daka.daka_post()
    # daka.daka_get()
    # print(daka.user_info)

# daka_url="https://timeapi.lawxp.com/api/Card/AddCardLog"
# get_url="https://timeapi.lawxp.com/api/App_My/GetPersonalData?companyId=461&userId=2103470328"
# # token="eyJhbGciOiJSUzI1NiIsImtpZCI6IkY5QjQwMjg2NDBENTdCMTRFQURBMkUwRTcyNjJFMjFFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3NTc0MTIxNjgsImV4cCI6MTg0MzgxMjE2OCwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYXd4cC5jb20iLCJjbGllbnRfaWQiOiJhcHAiLCJzdWIiOiIxMDEzMzRfaXN3ZWJvYTpGYWxzZV9pc3dlc2FsZTpGYWxzZV9pc2FnZW50OkZhbHNlIiwiYXV0aF90aW1lIjoxNzU3NDEyMTY4LCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6IjIxMDM0NzAzMjgiLCJuYW1lIjoiZ3VvamlhbmNoZW5nIiwiZ2l2ZW5fbmFtZSI6IumDreW7uuaIkCIsImVtYWlsIjoiZ3VvamNoQGxhd3hwLmNvbSIsImp0aSI6IjE0OEFCQkY2QTkxRThENjkwNzVFRDhDMkQ4N0E3QTJGIiwiaWF0IjoxNzU3NDEyMTY4LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbImN1c3RvbSJdfQ.QdDnRKH2m5F068INBaI1GTMaow5MdT7uSDVwVesRk_pwt6gZnDS1scNvhnMZgEQLjd2LybPD_77FN8FVajMHHemm_gjAbDRsBj1eD0UR2Z0JBe_xtmIEFF6brbKprgtxxx0qfyr3PeSvlwhSd-J7CD4ET9wrjAwHV7SI6_MIWPEdiYPsBEBnFkkHOKxCI_JVsZFRsDR5UfV3i6RHv_-Ww0qTTV3W2tYaktSJOzk6606TMCDBS3X3fLIOKdVJNtgASOgQuiTcezsvOO64nYY6wkOodF1M8fHlJMuZEVfXx3m8tv9Poj3R-J_uMDbISVqPUcJFK8mBorV0TkrJl9hzaw"
# token="eyJhbGciOiJSUzI1NiIsImtpZCI6IkY5QjQwMjg2NDBENTdCMTRFQURBMkUwRTcyNjJFMjFFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3NjAxNDI3OTAsImV4cCI6MTc2MTAwNjc5MCwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYXd4cC5jb20iLCJjbGllbnRfaWQiOiJjcm0iLCJzdWIiOiIxMDEzMzRfaXN3ZWJvYTpGYWxzZV9pc3dlc2FsZTpGYWxzZV9pc2FnZW50OkZhbHNlIiwiYXV0aF90aW1lIjoxNzYwMTQyNzkwLCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6IjIxMDM0NzAzMjgiLCJuYW1lIjoiZ3VvamlhbmNoZW5nIiwiZ2l2ZW5fbmFtZSI6IumDreW7uuaIkCIsImVtYWlsIjoiZ3VvamNoQGxhd3hwLmNvbSIsImp0aSI6IjA3Q0RDQTkzOUQ0MDk5RjQ4OUM4QUE4MEUwMThDNUUyIiwiaWF0IjoxNzYwMTQyNzkwLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIl0sImFtciI6WyJjdXN0b20iXX0.X29ElcH3dmi4MU6rx580zkeyniej1mnSE3BNb4lWxKVnwJ0YhZu0IRw7_XxK4jJvZFz2KMDQTIOX64UBSZPmp0JvZVRGZ9vA5mxG1x1YHxL2JN2zkXXnjpmstLn2VZ_0uTCMVNAQAFwDpyV-3rVcOouXr_yzT8X4FcAfHuSnSo2Cq4WxUUWAl5AstQkcwanXl47NwKANSn6aR2xqR8ltdSujLY1dzY96Ee9yVTX7wdgcxSmrPBQeX_P3rOW8RSwfSvpdkcUPtSXYs6NBc6kiPvHsVpjpM1c8A-3-RALbvyZ-DUP02wCrkSq0VH_kDh67nsyLF_04da26N1--zJ9M-Q"
# headers = {
#     "Content-Type": "application/json",
#     "User-Agent": "trust/5.0.294 (iPhone; iOS 18.6; Scale/3.00)",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Authorization":f"Bearer {token}"
# }
# form_data={
#     "ApprovalId":"",
#     "ApprovalInfoId":"",
#     "AttenceGroupId":"222",
#     "AttendanceTime":"18:00",
#     "CardAddress":"广东省广州市番禺区兴南大道靠近诺德天街",
#     "CardEquipment":"iPhone XS",
#     "CardResult":"",
#     "CardTime":"18:02:02",
#     "CardType":"0",
#     "CompanyId":"461",
#     "File":"",
#     "File2Id":"0",
#     "FileId":"0",
#     "IsAutomation":"false",
#     "IsSameAddr":"true",
#     "RelationId":"125",
#     "Remark":"",
#     "ShiftId":"181",
#     "ShiftTimeId":"236",
#     "ShiftTimeType":"2",
#     "UserId":"2103470328",
#     "WorkOrderId":"0",
#     "lat":"23.009195",
#     "lng":"113.351668"
# }	
# res=requests.post(daka_url,data=form_data,headers=headers)
# print(res.json())
# res=requests.get(get_url,headers=headers)
# print(res.json())
