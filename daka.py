
import requests


daka_url="https://timeapi.lawxp.com/api/Card/AddCardLog"
get_url="https://timeapi.lawxp.com/api/App_My/GetPersonalData?companyId=461&userId=2103470328"
# token="eyJhbGciOiJSUzI1NiIsImtpZCI6IkY5QjQwMjg2NDBENTdCMTRFQURBMkUwRTcyNjJFMjFFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3NTc0MTIxNjgsImV4cCI6MTg0MzgxMjE2OCwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYXd4cC5jb20iLCJjbGllbnRfaWQiOiJhcHAiLCJzdWIiOiIxMDEzMzRfaXN3ZWJvYTpGYWxzZV9pc3dlc2FsZTpGYWxzZV9pc2FnZW50OkZhbHNlIiwiYXV0aF90aW1lIjoxNzU3NDEyMTY4LCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6IjIxMDM0NzAzMjgiLCJuYW1lIjoiZ3VvamlhbmNoZW5nIiwiZ2l2ZW5fbmFtZSI6IumDreW7uuaIkCIsImVtYWlsIjoiZ3VvamNoQGxhd3hwLmNvbSIsImp0aSI6IjE0OEFCQkY2QTkxRThENjkwNzVFRDhDMkQ4N0E3QTJGIiwiaWF0IjoxNzU3NDEyMTY4LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbImN1c3RvbSJdfQ.QdDnRKH2m5F068INBaI1GTMaow5MdT7uSDVwVesRk_pwt6gZnDS1scNvhnMZgEQLjd2LybPD_77FN8FVajMHHemm_gjAbDRsBj1eD0UR2Z0JBe_xtmIEFF6brbKprgtxxx0qfyr3PeSvlwhSd-J7CD4ET9wrjAwHV7SI6_MIWPEdiYPsBEBnFkkHOKxCI_JVsZFRsDR5UfV3i6RHv_-Ww0qTTV3W2tYaktSJOzk6606TMCDBS3X3fLIOKdVJNtgASOgQuiTcezsvOO64nYY6wkOodF1M8fHlJMuZEVfXx3m8tv9Poj3R-J_uMDbISVqPUcJFK8mBorV0TkrJl9hzaw"
token="eyJhbGciOiJSUzI1NiIsImtpZCI6IkY5QjQwMjg2NDBENTdCMTRFQURBMkUwRTcyNjJFMjFFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3NTk5OTE0NzcsImV4cCI6MTc2MDg1NTQ3NywiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYXd4cC5jb20iLCJjbGllbnRfaWQiOiJjcm0iLCJzdWIiOiIxMDEzMzRfaXN3ZWJvYTpGYWxzZV9pc3dlc2FsZTpGYWxzZV9pc2FnZW50OkZhbHNlIiwiYXV0aF90aW1lIjoxNzU5OTkxNDc3LCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6IjIxMDM0NzAzMjgiLCJuYW1lIjoiZ3VvamlhbmNoZW5nIiwiZ2l2ZW5fbmFtZSI6IumDreW7uuaIkCIsImVtYWlsIjoiZ3VvamNoQGxhd3hwLmNvbSIsImp0aSI6IkJCQzNFNTdCQUU5NTRGNzFFNzcxQjMzODA1RTBCNTcxIiwiaWF0IjoxNzU5OTkxNDc3LCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIl0sImFtciI6WyJjdXN0b20iXX0.bymQXipR90x1Oc87-6o8YgLHrqwTUdzs0SF16sSO3SA7OSTi-3Xbj6ekzzs6Q16gZLtHuDJTxppw1qizaCRgBIuyeqa0nvFhRg40o-Zw6Zp0f6Unm52ClhZyyyX2nNxFvwi3zRwozEGc0r7UjGRQeQCL00sjDrSWRSor_NFyKIYJXFzeXsxgl_TgO0YQ7r0jpcKkfNCR-ULVuYNYec8RZBWR1PMrMoKUWvt3POCP0Rdc4U78EcakrBhCsyfGiRgt7IRAZZCdbjrNxoQ-hGMLU3CgCgla72JwsRkuiRn7kW9AY73xzHhutMm3TsBcF1b0_m38bTE3VlREnD9zyDrGsA"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "trust/5.0.294 (iPhone; iOS 18.6; Scale/3.00)",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization":f"Bearer {token}"
}
form_data={
    "ApprovalId":"",
    "ApprovalInfoId":"",
    "AttenceGroupId":"222",
    "AttendanceTime":"18:00",
    "CardAddress":"广东省广州市番禺区兴南大道靠近诺德天街",
    "CardEquipment":"iPhone XS",
    "CardResult":"",
    "CardTime":"18:02:02",
    "CardType":"0",
    "CompanyId":"461",
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
    "UserId":"2103470328",
    "WorkOrderId":"0",
    "lat":"23.009195",
    "lng":"113.351668"
}	
res=requests.post(daka_url,data=form_data,headers=headers)
print(res.json())
res=requests.get(get_url,headers=headers)
print(res.json())
