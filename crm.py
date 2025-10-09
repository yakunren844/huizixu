
import datetime
import requests
import re
import random
from datetime import timedelta

from requests_toolbelt import MultipartEncoder

class crm:
    user_info=None
    login_url="https://api1.likewon.cn/api/Token"
    customer_url="https://api1.likewon.cn/api/ProtectingCustomers/GetCustomerList"
    customer_detail_url="https://api1.likewon.cn/api/ProtectingCustomers/GetCustomerDetail"
    genjin_submit_url="https://api1.likewon.cn/api/CustomerSaleRecord/AddSaleRecord"
    limit_day=15

    genjin_json=[{'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20057','label_name':'意向','context':'微信推送了行业汇资需给客户，客户对此很感兴趣并进行了简短交流，有效维护了客情关系并挖掘新需求。'},
                 {'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20058','label_name':'考虑','context':'本周重点跟进。客户已收到方案，预计下周反馈；初步意向明确，正安排测试跟进。'},
                 {'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20060','label_name':'无兴趣','context':'客户明确表示现阶段对【司法大数据/汇资需】产品无进一步需求。原因主要为暂不适用。已礼貌回应。'},
                 {'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20075','label_name':'约见中','context':'客户原则上同意会面，需与其团队确认时间。计划再跟进确认最终时间和约见地点。'},
                 {'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20090','label_name':'谈合作','context':'客户未直接拒绝，但回应“暂时不需要，有需求联系”。判断为意向度较低。已发送节日祝福结束对话，计划将其纳入季度通用产品资讯的推送名单'},
                 {'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20114','label_name':'考虑合作','context':'客户态度开放，但希望先了解更多信息再决定是否见面。已发送产品介绍及成功案例，以后跟进反馈，再推动约见。'},
                 {'p_name':'微信','p_id':'20056','followUpType':'101309','label_id':'20116','label_name':'有待考虑','context':'向客户完整传达了产品核心价值。对方暂未回。判断为信息已送达但未激发即时需求。无需过度跟进，计划以分享一篇相关行业报告进行破冰'},
                 {'p_name':'邮箱','p_id':'20053','followUpType':'101305','label_id':'20054','label_name':'发送成功','context':'通过电子邮件发送了汇资需资料和公司介绍给客户，同时介绍了汇资需的优势，挖掘新需求。'},
                 {'p_name':'电话','p_id':    '2','followUpType':'101301','label_id':'20120','label_name':'电话沟通','context':'电话跟进。客户个人认可价值，但表示需“财务和业务部门共同决策”，推进阻力大。判断当前非合适时机。'},
                 {'p_name':'电话','p_id':'20062','followUpType':'101301','label_id':'20063','label_name':'有效沟通','context':'接触人非最终决策者，且对产品理解不深，无法有效内部推动。已礼貌结束沟通，请求在有明确需求时引荐相关负责人。'},
                 {'p_name':'电话','p_id':'20062','followUpType':'101301','label_id':'20067','label_name':'意向','context':'客户未直接拒绝，但回应“暂时不需要，有需求联系”。判断为意向度较低。计划将其纳入用产品资讯的推送名单，保持曝光。'},
                 {'p_name':'电话','p_id':'20062','followUpType':'101301','label_id':'20068','label_name':'考虑','context':'电话跟进。客户透露已与竞品合作多年，关系稳定，切换成本高。未强行推销，转而请教其选择标准，获得了宝贵信息。'},
                 ]

    def __init__(self):
        pass
    def extract_integers(self,text):
        """提取字符串开头的整数部分"""
        match = re.match(r'-?\d+', text)
        return int(match.group()) if match else 0
    def get_json(self,url,params=None):
        

        return self.json    
    def get_random_time_period(self):
        # 随机选择今天或昨天
        is_today = random.choice([True, False])
        
        if is_today:
            # 今天
            base_date = datetime.date.today()
            now = datetime.datetime.now()
            
            # 今天开始时间：09:00
            start_of_day = datetime.datetime.combine(base_date, datetime.time(9, 0))
            
            # 结束时间为当前时间，但不能早于09:00
            end_time = max(start_of_day, now - timedelta(minutes=20))
            
            # 随机开始时间在09:00到(结束时间-10分钟)之间
            max_start_time = end_time - timedelta(minutes=10)
            random_start = start_of_day + timedelta(
                seconds=random.randint(0, int((max_start_time - start_of_day).total_seconds()))
            )
            
        else:
            # 昨天
            base_date = datetime.date.today() - timedelta(days=1)
            
            # 昨天时间范围：09:30至18:00
            start_of_day = datetime.datetime.combine(base_date, datetime.time(9, 30))
            end_of_day = datetime.datetime.combine(base_date, datetime.time(18, 0))
            
            # 随机持续时间10-20分钟
            duration = timedelta(minutes=random.randint(10, 20))
            
            # 确保开始时间+持续时间不超过18:00
            max_start_time = end_of_day - duration
            
            # 随机开始时间
            random_start = start_of_day + timedelta(
                seconds=random.randint(0, int((max_start_time - start_of_day).total_seconds()))
            )
        
        # 计算结束时间
        duration_minutes = random.randint(10, 40)
        duration_seconds = random.randint(0, 60)
        random_end = random_start + timedelta(minutes=duration_minutes, seconds=duration_seconds)
    
        # 分别返回日期、开始时间、结束时间
        date_str = random_start.strftime('%Y-%m-%d')
        start_time_str = random_start.strftime('%H:%M:%S')
        end_time_str = random_end.strftime('%H:%M:%S')
        
        return date_str, start_time_str, end_time_str
    
    def login(self,username,password):
        json_data={
            "account": username,
            "password": password,
            "type": 3
            }
        res=requests.post(self.login_url,json=json_data)
        if res.status_code==200 and res.json()['code']==0:
            self.user_info=res.json()['data']
        else:
            self.user_info=None
            
        print(self.user_info)
    def genjin(self,customer_list):
        for customer in customer_list:
            remain_day=self.extract_integers(customer['waitMarketerCountdown'])
            print(customer['companyName'],",剩余天数:",remain_day)
            if remain_day<self.limit_day:
                detail=self.get_customer_detail(customer['customerId'])
                customerContactsList=detail['customerContactsList']
                if len(customerContactsList)>0:
                    contactsId=customerContactsList[0]['contactsId']
                    
                    self.genjin_submit(customer['customerId'],contactsId)
                    print("客户：",customer['companyName'],"提交跟进")
                else:
                    print("客户：",customer['companyName'],"无联系人")
                
    def genjin_submit(self,customer_id,contactId):
        saleUserId=self.user_info['saleUserId']
        token=self.user_info['accessToken']
        label=random.choice(self.genjin_json)
       
        
        day_str,start_time,end_time=self.get_random_time_period()
        
        multipart_data = MultipartEncoder(
            fields={
                'customerId':str(customer_id),
                'saleUserId':str(saleUserId),
                'contactId':str(contactId),
                'description':label['context'],
                'followUpType':str(label['followUpType']),
                'lineId':str(2),
                'recordId':str(0),
                'delFileId':'',
                'followupDate':day_str,
                'followBegionTime':start_time,
                'followEndTime':end_time,
                'flagIds':str(label['label_id']),
            }
        )
        headers={
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': multipart_data.content_type,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        
        res=requests.post(self.genjin_submit_url,data=multipart_data,headers=headers)
        if res.status_code==200 and res.json()['code']==0:
            print("客户：",customer_id,"提交跟进成功")
        else:
            print("客户：",customer_id,"提交跟进失败")
        # print(res.json())
        
    def get_customer_detail(self,customer_id):
        token=self.user_info['accessToken']
        headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        params={
            'CustomerId':customer_id,
            'LineId':2,
            'SaleUserId':self.user_info['saleUserId'],
            'state':100002,
        }
        res=requests.get(self.customer_detail_url,params=params,headers=headers)
        if res.status_code==200 and res.json()['code']==0:
            return res.json()['data']
        else:   
            return None
        
    def get_customer_list(self):
        customer_list=[]
        params_data={
            "pageIndex": 1,
            "Scope": 0,
            'LineId':2,
            'CompanyName':'',
            'State':100002
            }
        cur_page=1
        token=self.user_info['accessToken']
        headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        while True:
            # print(cur_page)
            params_data['pageIndex']=cur_page
            # print(params_data)
            res=requests.get(self.customer_url,params=params_data,headers=headers)
            # print(res.json())
            if res.status_code==200 and res.json()['code']==0:
                c_list=res.json()['data']['customerList']
                if len(c_list)>0:
                    customer_list.extend(c_list)
                else:
                    break
            else:
                break
            cur_page+=1
        # print('----------------------------')
        # print(customer_list)
        # print('----------------------------')
        return customer_list
    def get_expire_customer(self):
        pass

if __name__ == '__main__':
    crm=crm()
    # day_str,start_time,end_time=crm.get_random_time_period()
    # print(day_str,start_time,end_time)
    # crm.login("liuhaixia","huifa888")
    # crm.login("hanfeng@lawxp.com","654321")
    crm.login("guojiancheng","Gjc523220313")
    customer_list=crm.get_customer_list()
    print(customer_list)
    crm.genjin(customer_list)
    # crm.genjin_submit('9685763841447336','9609869859444000')
