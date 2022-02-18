import requests
import json

import requests
from datetime import datetime, timedelta, timezone, date
import pytz
tz = pytz.timezone("Etc/UTC")

def getValue(_list, value, determine = 0):
    try:
        if value in _list:
            if determine != 0:
                try:
                    return _list[value] / 1000
                except:
                    return _list[value]
            else:             
                return _list[value]
    except:
        pass
    return None

def fanduel_scrape_market(data):
    try:
        _api = data["link"]
        mlb = data["mlb"]        

        session = requests.Session()
        response = session.request("GET", _api)
        result = json.loads(response.text.encode('utf8'))

        selectionInfo = []

        marketNameList = ['Spread Betting', 'Total Points', 'Moneyline', 'Alternative Spreads', 'Spread', 'Total Match Points', 'Alternate Spread', 'Puck Line', 'Total Goals']
        for market_id in result['attachments']['markets']:      
            try:      
                market = result['attachments']['markets'][market_id]            
                
                if market['marketName'] in marketNameList or mlb == True or 'Alternate Spread' in market['marketName']:
                    for selection in market["runners"]:
                        market_type = market['marketName']

                        if market_type == "Total Points" or market_type == 'Total Match Points' or market_type == 'Total Goals':
                            market_type = 'Total'
                        elif market_type == "Moneyline":
                            market_type = 'Moneyline'
                        elif market_type == "Spread Betting" or market_type == "Spread" or market_type == 'Puck Line':
                            market_type = 'Spread'
                        elif market_type == "Alternative Spreads" or market_type == "Alternate Spread" or 'Alternate Spread' in market['marketName']:
                            market_type = 'Alternative Spread'

                        elif mlb == False:                                
                            continue

                        print(market_type)

                        eventId = market['eventId']
                        if mlb == True:
                            eventId = market['marketId']

                        selectionInfo.append({
                            "self_selection_id": selection["selectionId"],
                            "market_type": market_type,
                            "line": getValue(selection, "handicap"),
                            "name": selection["runnerName"],
                            "eventId": eventId,
                            "self_market_id": market["marketId"],
                            "updateTime": datetime.now(tz),
                            "odds": selection["winRunnerOdds"]["trueOdds"]["decimalOdds"]["decimalOdds"],
                            "oddsAmerican": selection["winRunnerOdds"]["americanDisplayOdds"]["americanOdds"],
                            "self_event_id": eventId
                        })
                        
            except Exception as g:
                print(str(g))
                pass
        print(selectionInfo)
        print(data["link"], len(selectionInfo))
        
    except Exception as g:
        print(str(g))
        pass

data = {
    'link' : 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId=31246207',
    'mlb': False
}
fanduel_scrape_market(data)
# url = "https://portal.winningedgeinvestments.com/account/login/?returnurl=/"

# payload={'Username': 'jacobma.racingbb@gmail.com',
# 'Password': 'RACINGBB88',
# '__RequestVerificationToken': 'CfDJ8Iissb_G2MpCguzq4p4Ogr6NkHz6VTqYtu39VsxBVbgVWeGu58__nDdjWQS1wqJVSBeiaI2FZ470QQQ8oR6BMR6DvtskHkb6qq11fHl0NTXiRiHkupnWvtHnrKHxKRWYXx9h6uQ0_ZFOFU_gMIiktuY'}
# files=[

# ]
# # headers = {
# #   'Cookie': '.AspNetCore.Antiforgery.SsJcyjhOR8k=CfDJ8Iissb_G2MpCguzq4p4Ogr6TYSqzld3RAuJJxgZarY4npUVP76iBqdAStbvRNcJbZY86U660RIrql8sC6cLo8JA5nbO-SUKX7C5cOOctue1AppnT3gFO7D7u3pIKHYNW84f2OfHVC_JmDZv3LEChnpE; ARRAffinity=72074257a43aa4a5544d0481fd21539477f55378e3e32b7beb598b12cf08c8c1; ARRAffinitySameSite=72074257a43aa4a5544d0481fd21539477f55378e3e32b7beb598b12cf08c8c1; mewantcookieauth=CfDJ8Iissb_G2MpCguzq4p4Ogr6whKp2dwoSA11EETEUxzTwUEaBn55nyF2sFuYkHizVOarrGI4-JxzlYmbv9YxAlDzA7vAQp0MIh5SUOZA9R3v1Je53KWqebgZ2pnFBGGHcjYJJRTv5ojV3zY1z0OHj2xMFIYS_mV3N6OUNzWzzevpBr0MvDWwfmCoNoBhC6hbATqv4BjPBVu2YdF8giCCAdzQkZUyotnTRHr7mH4XDDO1y3R-MHFbqjb-sM2-WUbI2XlISPA28xpDA-DPE2ShOnP8DhppEIci3oYFPBtN37zEskrYA-HItUrS835hGTqYyVcorm-S4eWh9W7rbvRZQlHo'
# # }

# session = requests.Session()
# response = session.request("POST", url, data=payload, files=files)

# payload = json.dumps({
#     "start": 0,
#     "length": 50,
#     "isFiltered": False,
#     "productList": "" ,
#     "fromDateString": "11/2/2022",
#     "toDateString": "11/2/2022",
#     "searchValue": "" 
# })


# api = "https://portal.winningedgeinvestments.com/api/member/messages/datatablefilter/?start=0&length=10&isFiltered=false&productList=&fromDateString=11%2F2%2F2022&toDateString=11%2F2%2F2022&searchValue="

# response = session.request("GET", api)

# print(response.text)