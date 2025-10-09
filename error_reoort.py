import requests


get_error_url="https://timeapi.lawxp.com/api/Report/GetReportDetail"
report_url="https://timeapi.lawxp.com/api/Report/AddReport"
token="eyJhbGciOiJSUzI1NiIsImtpZCI6IkY5QjQwMjg2NDBENTdCMTRFQURBMkUwRTcyNjJFMjFFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3NTc0MTIxNjgsImV4cCI6MTg0MzgxMjE2OCwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYXd4cC5jb20iLCJjbGllbnRfaWQiOiJhcHAiLCJzdWIiOiIxMDEzMzRfaXN3ZWJvYTpGYWxzZV9pc3dlc2FsZTpGYWxzZV9pc2FnZW50OkZhbHNlIiwiYXV0aF90aW1lIjoxNzU3NDEyMTY4LCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6IjIxMDM0NzAzMjgiLCJuYW1lIjoiZ3VvamlhbmNoZW5nIiwiZ2l2ZW5fbmFtZSI6IumDreW7uuaIkCIsImVtYWlsIjoiZ3VvamNoQGxhd3hwLmNvbSIsImp0aSI6IjE0OEFCQkY2QTkxRThENjkwNzVFRDhDMkQ4N0E3QTJGIiwiaWF0IjoxNzU3NDEyMTY4LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbImN1c3RvbSJdfQ.QdDnRKH2m5F068INBaI1GTMaow5MdT7uSDVwVesRk_pwt6gZnDS1scNvhnMZgEQLjd2LybPD_77FN8FVajMHHemm_gjAbDRsBj1eD0UR2Z0JBe_xtmIEFF6brbKprgtxxx0qfyr3PeSvlwhSd-J7CD4ET9wrjAwHV7SI6_MIWPEdiYPsBEBnFkkHOKxCI_JVsZFRsDR5UfV3i6RHv_-Ww0qTTV3W2tYaktSJOzk6606TMCDBS3X3fLIOKdVJNtgASOgQuiTcezsvOO64nYY6wkOodF1M8fHlJMuZEVfXx3m8tv9Poj3R-J_uMDbISVqPUcJFK8mBorV0TkrJl9hzaw"
companyId='461'
UserId='2103470328'

def error_report(companyId,postUserId,err_list):
    reportRecord=[]
    if len(err_list)==0 or not err_list:
        return
    
    for item in err_list:
        re_item={
            "cardLogBadId":item["cardLogBadId"],
            "cardTime":item["cardTime"],
            "isChoose":True,
            "statutes":2,
            "tag":item["tag"],
            "type":item["type"]
        }
        reportRecord.append(re_item)
    re_json={
        "companyId":companyId,
        "postUserId":postUserId,
        "remark":"系统错误",
        "reportRecord":reportRecord
    }
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'trust/5.0.294 (iPhone; iOS 18.6; Scale/3.00)'
    }
    res=requests.post(report_url,json=re_json,headers=headers)
    print(res.json())
def get_day_error(companyId,UserId,error_day):
    # ?EndTime=2025-09-03&
    # PageIndex=3&
    # PageSize=15&
    # StartTime=2025-09-03
    # &Type=-1&
    # UserId=2103470328&
    # companyId=461
    params={
        "StartTime":error_day,
        "EndTime":error_day,
        "PageIndex":1,
        "PageSize":60,
        "Type":-1,
        "UserId":UserId,
        "companyId":companyId

    }
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'trust/5.0.294 (iPhone; iOS 18.6; Scale/3.00)'
        
    }
    res=requests.get(get_error_url,params=params,headers=headers)
    # print(res.json())
    return res.json()['data']['data']
def month_error(year,month):
    days = [str(i).zfill(2) for i in range(1, 32)]
    month = str(month).zfill(2)
    for day in days:
        error_day=f"{year}-{month}-{day}"
        print(error_day)
        # error_list=get_day_error(companyId,UserId,error_day)
        # error_report(companyId,UserId,error_list)
    
# deal_day="2025-09-30"
# error_list=get_day_error(companyId,UserId,deal_day)
# print(error_list)
# error_report(companyId,UserId,error_list)
month_error(2025,9)