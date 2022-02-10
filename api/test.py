import requests
import json

import requests

url = "https://portal.winningedgeinvestments.com/account/login/?returnurl=/"

payload={'Username': 'jacobma.racingbb@gmail.com',
'Password': 'RACINGBB88',
'__RequestVerificationToken': 'CfDJ8Iissb_G2MpCguzq4p4Ogr6NkHz6VTqYtu39VsxBVbgVWeGu58__nDdjWQS1wqJVSBeiaI2FZ470QQQ8oR6BMR6DvtskHkb6qq11fHl0NTXiRiHkupnWvtHnrKHxKRWYXx9h6uQ0_ZFOFU_gMIiktuY'}
files=[

]
# headers = {
#   'Cookie': '.AspNetCore.Antiforgery.SsJcyjhOR8k=CfDJ8Iissb_G2MpCguzq4p4Ogr6TYSqzld3RAuJJxgZarY4npUVP76iBqdAStbvRNcJbZY86U660RIrql8sC6cLo8JA5nbO-SUKX7C5cOOctue1AppnT3gFO7D7u3pIKHYNW84f2OfHVC_JmDZv3LEChnpE; ARRAffinity=72074257a43aa4a5544d0481fd21539477f55378e3e32b7beb598b12cf08c8c1; ARRAffinitySameSite=72074257a43aa4a5544d0481fd21539477f55378e3e32b7beb598b12cf08c8c1; mewantcookieauth=CfDJ8Iissb_G2MpCguzq4p4Ogr6whKp2dwoSA11EETEUxzTwUEaBn55nyF2sFuYkHizVOarrGI4-JxzlYmbv9YxAlDzA7vAQp0MIh5SUOZA9R3v1Je53KWqebgZ2pnFBGGHcjYJJRTv5ojV3zY1z0OHj2xMFIYS_mV3N6OUNzWzzevpBr0MvDWwfmCoNoBhC6hbATqv4BjPBVu2YdF8giCCAdzQkZUyotnTRHr7mH4XDDO1y3R-MHFbqjb-sM2-WUbI2XlISPA28xpDA-DPE2ShOnP8DhppEIci3oYFPBtN37zEskrYA-HItUrS835hGTqYyVcorm-S4eWh9W7rbvRZQlHo'
# }

session = requests.Session()
response = session.request("POST", url, data=payload, files=files)

payload = json.dumps({
    "start": 0,
    "length": 50,
    "isFiltered": False,
    "productList": "" ,
    "fromDateString": "11/2/2022",
    "toDateString": "11/2/2022",
    "searchValue": "" 
})


api = "https://portal.winningedgeinvestments.com/api/member/messages/datatablefilter/?start=0&length=10&isFiltered=false&productList=&fromDateString=11%2F2%2F2022&toDateString=11%2F2%2F2022&searchValue="

response = session.request("GET", api)

print(response.text)