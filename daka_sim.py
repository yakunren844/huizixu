
from datetime import datetime
import requests
from datetime import datetime

class Daka:
    CompanyId="461"
    login_url="https://api1.likewon.cn/api/Token"
    daka_url="https://timeapi.lawxp.com/api/Card/AddCardLog"
    daka_get_url="https://timeapi.lawxp.com/api/Card/AddCardLogBad"
    get_url="https://timeapi.lawxp.com/api/App_My/GetPersonalData?companyId=461&userId=2103470328"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "trust/5.0.294 (iPhone; iOS 18.6; Scale/3.00)",
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
   

if __name__ == '__main__':
#     # uvicorn.run(app, host="0.0.0.0", port=9108)
    daka=Daka()
    daka.login("guojiancheng","Gjc523220313")
    daka.daka_post()
   