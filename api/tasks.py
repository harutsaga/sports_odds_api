from celery import shared_task
from api.models import Event, Selection, Market, BookieEvent, SportsType, League, MarketType, Bookie
from api.serializers import EventSerializer, BookieEventSerializer, BookieLinkSerializer
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool 
import traceback
import time
from dateutil import parser, tz
from datetime import datetime, timedelta, timezone, date
import pytz
from django.db.models import Q
import sys

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

# replace the string
def replaceDeter(_name):
    try:
        _name = _name.replace('@','-').replace('vs','-')
    except:
        pass

    return _name

def replaceString(name):
        name = name.replace('AL ','American League ').replace('NL ','National League ')
        return name

# save the selection information
def saveSelectionInfo(_selectionInfo):
    try:        
        for _selection in _selectionInfo:
            
            try:
                
                selection = None

                try:
                    selection = Selection.objects.get(self_selection_id=_selection['self_selection_id'], self_market_id=_selection['self_market_id'])
                except:
                    pass

                if selection is None:                    
                    r = Selection(self_event_id=_selection['self_event_id'], self_market_id=_selection['self_market_id'], name=_selection['name'],odds=_selection['odds'],oddsAmerican=_selection['oddsAmerican'],line=_selection['line'],self_selection_id=_selection['self_selection_id'],updateTime=datetime.now(tz))
                    r.save()

                    market = None

                    try:
                        market = Market.objects.get(self_market_id=_selection['self_market_id'], self_event_id=_selection['self_event_id'])
                    except:
                        pass

                    if market is None:
                        market = Market(self_market_id=_selection['self_market_id'], market_type=_selection['market_type'], self_event_id=_selection['self_event_id'])
                        market.save()

                    market.selection.add(r)
                    market.save()
                    

                else:
                    if selection.odds == _selection['odds'] and selection.line == _selection['line']:
                        selection.updateTime = datetime.now(tz)
                        selection.save()

                        pass

                    selection.odds = _selection['odds']
                    selection.oddsAmerican = _selection['oddsAmerican']
                    selection.line = _selection['line']
                    # selection.name = _selection['name']
                    selection.updateTime = datetime.now(tz)
                    selection.save()

            except:                
                pass
    except:
        pass

# save the event info
def saveBookieEvent(_eventList, bookieType):
    try:
        for event in _eventList:
            try:
                comp = None

                delta = timedelta(minutes=30)

                if event['league'] == League.MLB:
                    delta = timedelta(hours=24)

                name = replaceDeter(event['name'])
                
                try:
                    try:
                        if event['league'] == League.MLB:
                            comp = Event.objects.get(sports=event['sports'], league=event['league'], name=name)
                        else:
                            comp = Event.objects.get(startTime__range=(event['startTime'] - delta, event['startTime'] + delta), sports=event['sports'], league=event['league'], name=name)
                    except:
                        pass

                    if comp is None:                        
                        try:
                            comp = Event.objects.get(startTime__range=(event['startTime'] - delta, event['startTime'] + delta), sports=event['sports'], league=event['league'], full_name=name)
                        except:
                            pass

                    if comp is None and event['league'] != League.MLB:
                        try:
                            _splitNames = name.split('-')

                            _home = ""
                            _away = ""

                            if len(_splitNames) == 2:
                                _home = _splitNames[1].strip()
                                _away = _splitNames[0].strip()

                                _home = _home.split(" ")
                                _away = _away.split(" ")

                                del _home[0]
                                del _away[0]

                                _home = " ".join(_home)
                                _away = " ".join(_away)
                                
                                comp = Event.objects.get(startTime__range=(event['startTime'] - delta, event['startTime'] + delta), sports=event['sports'], league=event['league'], awayName__contains=_away, homeName__contains=_home)
                        except:
                            pass

                    # if comp is None:
                    #     print(name, event,bookieType)
                    
                    if comp is not None:
                        count = BookieEvent.objects.filter(self_event_id=event['eventId'], bookie=bookieType).count()
                        if count == 0:
                            r = BookieEvent(event=comp, self_event_id=event['eventId'], bookie=bookieType)                            
                            r.save()                        
                except:                    
                    pass
            except:
                pass
    except:
        # print(traceback.format_exc())
        pass

# get the base event info
def get_event_info(_url, _sports, _league):
    try:
        session = requests.Session()
        response = session.request("GET", _url)
        result = json.loads(response.text.encode('utf8'))    

        eventList = []
        for _event in result['events']:            
            try:
                full_name = None

                try:
                    full_name = _event['event']['englishName']
                    f = full_name.split('-')
                    full_name = f"{f[1]} - {f[0]}".strip()
                except:
                    pass

                eventList.append({
                    "eventId": _event['event']['id'],
                    "name": replaceDeter(_event['event']['name']),
                    "full_name": full_name,
                    "startTime": parser.parse(_event['event']["start"]),
                    "updateTime": datetime.now(tz),
                    "awayName": getValue(_event['event'],"awayName"),
                    "homeName": getValue(_event['event'],"homeName"),
                    "sports": _sports,
                    "league": _league
                })              
            except:                
                pass

        for event in eventList:
            try:
                count = Event.objects.filter(e_id=event['eventId']).count()

                if count == 0:
                    r = Event(full_name=event['full_name'], e_id=event['eventId'], name=event['name'], startTime=event['startTime'], updateTime=event['updateTime'], awayName=event['awayName'], homeName=event['homeName'], sports=event['sports'], league=event['league'])
                    r.save()
                else:
                    _e = Event.objects.get(e_id=event['eventId'])
                    _e.startTime = event['startTime']
                    _e.updateTime = event['updateTime']
                    _e.full_name = event['full_name']
                    _e.name = event['name']
                    _e.save()
            except:                
                pass
    except:        
        pass

baseEventFlag = False

# every 1 hour    
@shared_task
def get_base_event():
    global baseEventFlag

    if baseEventFlag == True:
        return

    baseEventFlag = True

    try:
        _time = int(time.time() *1000)

        # nba
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/basketball/nba.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"                        
        get_event_info(_api, SportsType.BASKETBALL, League.NBA)

        # nfl
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/american_football/nfl.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"
        get_event_info(_api, SportsType.FOOTBALL, League.NFL)

        # mlb
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/baseball.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"
        get_event_info(_api, SportsType.BASEBALL, League.MLB)

        # nhl
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/ice_hockey/nhl.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"
        get_event_info(_api, SportsType.ICE_HOCKEY, League.NHL)

    except:
        pass

    baseEventFlag = False


def draftking_get_event_info( _url, _sports, _league, flag = True):
    eventList = []
    try:
        session = requests.Session()
        response = session.request("GET", _url)
        result = json.loads(response.text.encode('utf8'))    
        
        if _league == League.MLB and flag == True:
            for offerCategorie in result['eventGroup']['offerCategories']:
                if offerCategorie['name'] == 'Team Futures':
                    for subcategory in offerCategorie['offerSubcategoryDescriptors']:
                        try:
                            subcategoryId = subcategory['subcategoryId']
                            categoryId = offerCategorie['offerCategoryId']

                            _api = f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670847/categories/{categoryId}/subcategories/{subcategoryId}?format=json"
                            eventList = eventList + draftking_get_event_info(_api, _sports, _league, False)
                        except:
                            pass

        else:                            
            for event in result['eventGroup']['events']:
                name = event["name"]
                
                try:                    
                    if _league == League.MLB:
                        name = name.replace('MLB','').strip()

                    if name[0].isdigit():
                        name = "World Series " + name
                except:
                    pass
                    
                eventList.append({
                    "eventId": event["providerEventId"],
                    "name": replaceDeter(name),
                    "startTime": parser.parse(event["startDate"]),
                    "sports": _sports,
                    "league": _league
                })
    
    except:
        pass

    return eventList

def fanduel_get_event_info(_url, _sports, _league):
    eventList = []
    try:
        session = requests.Session()
        response = session.request("GET", _url)
        result = json.loads(response.text.encode('utf8'))    
        
        if _league == League.MLB:
            for market_id in result['attachments']['markets']:            
                try:
                    event = result['attachments']['markets'][market_id]        
                    
                    name = event["marketName"].replace('MLB','')                        
                    name = replaceString(name)

                    if '-' in name:
                        f = name.split('-')[1].strip()
                        
                        if f[0].isdigit():
                            name = name.replace('- ','')
                        else:
                            name = name.split('-')[0].strip()

                    eventList.append({
                        "eventId": market_id,
                        "name": name,
                        "startTime": parser.parse(event["marketTime"]), 
                        "sports": _sports,
                        "league": _league
                    })
                except Exception as f:
                    pass            
        else:
            for event_id in result['attachments']['events']:            
                try:
                    event = result['attachments']['events'][event_id]        
                    
                    eventList.append({
                        "eventId": event_id,
                        "name": replaceDeter(event["name"]),
                        "startTime": parser.parse(event["openDate"]), 
                        "sports": _sports,
                        "league": _league
                    })
                except:
                    pass
        
    except:        
        pass

    return eventList

# twinspires event
def twinspires_get_event_info(_url, _sports, _league):
    eventList = []
    try:
        session = requests.Session()
        response = session.request("GET", _url)
        result = json.loads(response.text.encode('utf8'))    
        
        for _event in result['events']:            
            try:
                eventList.append({
                    "eventId": _event['event']['id'],
                    "name": replaceDeter(_event['event']['name']),
                    "startTime": parser.parse(_event['event']["start"]),
                    "updateTime": datetime.now(tz),
                    "awayName": getValue(_event['event'],"awayName"),
                    "homeName": getValue(_event['event'],"homeName"),
                    "sports": _sports,
                    "league": _league
                })
            except:                
                pass            
    except:        
        pass

    return eventList

bookieEventFlag = False

@shared_task
def get_bookie_event():
    # get the event info from draftkings

    global bookieEventFlag
    if bookieEventFlag == True:
        return

    bookieEventFlag = True
    try:
        _list = []        

        # nba
        _api = f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670846?format=json"
        _list1 = draftking_get_event_info(_api, SportsType.BASKETBALL, League.NBA)
        _list = _list + _list1

        # nfl
        _api = f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670561?format=json"
        _list2 = draftking_get_event_info(_api, SportsType.FOOTBALL, League.NFL)
        _list = _list + _list2

        # mlb
        _api = f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670847?format=json"
        _list3 = draftking_get_event_info(_api, SportsType.BASEBALL, League.MLB)
        _list = _list + _list3

        # nhl
        _api = f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670853?format=json"
        _list4 = draftking_get_event_info(_api, SportsType.ICE_HOCKEY, League.NHL)
        _list = _list + _list4
                        
        saveBookieEvent(_list, Bookie.DRAFTKING)
    except:
        pass    

    # get the event info from fanduel
    try:
        _list = []

        # nba
        _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=CUSTOM&customPageId=nba"
        _list1 = fanduel_get_event_info(_api, SportsType.BASKETBALL, League.NBA)
        _list = _list + _list1

        # # nfl
        _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=CUSTOM&customPageId=nfl"
        _list2 = fanduel_get_event_info(_api, SportsType.FOOTBALL, League.NFL)
        _list = _list + _list2

        # mlb
        _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=SPORT&eventTypeId=7511"
        _list3 = fanduel_get_event_info(_api, SportsType.BASEBALL, League.MLB)
        _list = _list + _list3

        # nhl
        _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=CUSTOM&customPageId=nhl"
        _list4 = fanduel_get_event_info(_api, SportsType.ICE_HOCKEY, League.NHL)
        _list = _list + _list4

        saveBookieEvent(_list, Bookie.FANDUEL)
    except:
        pass


    # get the event from twinspires
    try:
        _time = int(time.time() *1000)

        _list = []

        # nba
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/basketball/nba.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"                        
        _list1 = twinspires_get_event_info(_api, SportsType.BASKETBALL, League.NBA)

        _list = _list + _list1

        # nfl
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/american_football/nfl.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"
        _list2 = twinspires_get_event_info(_api, SportsType.FOOTBALL, League.NFL)
        _list = _list + _list2

        # mlb
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/baseball.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"
        _list3 = twinspires_get_event_info(_api, SportsType.BASEBALL, League.MLB)
        _list = _list + _list3

        # nhl
        _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/listView/ice_hockey/nhl.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&useCombined=true"
        _list4 = twinspires_get_event_info(_api, SportsType.ICE_HOCKEY, League.NHL)
        _list = _list + _list4
        
        saveBookieEvent(_list, Bookie.TWINSPIRES)
    except:
        pass

    bookieEventFlag = False        

# get the market info from draftkings
def draftkings_scrape_market(data):
    try:            
        _api = data["link"]
        mlb = data["mlb"]        

        session = requests.Session()
        response = session.request("GET", _api)
        result = json.loads(response.text.encode('utf8'))

        selectionInfo = []

        for category in result['eventGroup']['offerCategories']:
            try:
                if category['name'] != 'Game Lines' and mlb == False:
                    continue

                for sub_category in category['offerSubcategoryDescriptors']:
                    try:
                        
                        if sub_category['name'] == 'Game' or sub_category['name'] == 'Alternate Spread' or sub_category['name'] == 'Alternate Puck Line' or mlb == True:                                                    
                            
                            for events in sub_category['offerSubcategory']['offers']:                            
                                for market in events:
                                    for selection in market["outcomes"]:
                                        try:
                                            market_type = market["label"]

                                            if market_type == "Total":
                                                market_type = MarketType.TOTAL
                                            elif market_type == "Moneyline":
                                                market_type = MarketType.MONEYLINE
                                            elif market_type == "Spread" or market_type == "Puck Line":
                                                market_type = MarketType.SPREAD
                                            elif market_type == "Spread Alternate" or market_type == "Alternate Puck Line":
                                                market_type = MarketType.ALTERNATIVE_SPREAD

                                            elif mlb == False:                                                
                                                continue

                                            selectionInfo.append({
                                                "self_selection_id": selection["providerOutcomeId"],
                                                "market_type": market_type,
                                                "line": getValue(selection, "line"),
                                                "name": selection["label"],
                                                "eventId": market['providerEventId'],
                                                "self_market_id": market["providerOfferId"],
                                                "updateTime": datetime.now(tz),                                                
                                                "odds": selection["oddsDecimal"],
                                                "oddsAmerican": selection["oddsAmerican"],
                                                "self_event_id": market['providerEventId']
                                            })
                                        except:                                            
                                            pass
                    except Exception as h:
                        pass


            except Exception as e:                
                pass
                
        saveSelectionInfo(selectionInfo)
        
        # print("started..........")
    except:
        pass

M_DRAFT_MLB_FLAG = False        

@shared_task
def get_draftkings_market_mlb():
    global M_DRAFT_MLB_FLAG
    if M_DRAFT_MLB_FLAG == True:
        return
        
    M_DRAFT_MLB_FLAG = True

    while (True):
        try:
            _api = "https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670847?format=json"
            session = requests.Session()
            response = session.request("GET", _api)
            result = json.loads(response.text.encode('utf8'))   

            _list = []

            try:
                for offerCategorie in result['eventGroup']['offerCategories']:
                    if offerCategorie['name'] == 'Team Futures':
                        for subcategory in offerCategorie['offerSubcategoryDescriptors']:
                            try:
                                subcategoryId = subcategory['subcategoryId']
                                categoryId = offerCategorie['offerCategoryId']

                                _list.append({
                                    "link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670847/categories/{categoryId}/subcategories/{subcategoryId}?format=json", "mlb": True})
                            except:
                                pass
            except:
                pass

            try:        
                pool = ThreadPool(5)
                pool.starmap_async(draftkings_scrape_market, zip(_list))
                pool.close()
                pool.join()

                # for item in _list:
                #     draftkings_scrape_market(item)
                    
            except Exception as f:            
                pass

        except: 
            pass
        
    M_DRAFT_MLB_FLAG = False

M_DRAFT_NBA_FLAG = False

@shared_task
def get_draftkings_market_nba():

    global M_DRAFT_NBA_FLAG
    if M_DRAFT_NBA_FLAG == True:
        return

    M_DRAFT_NBA_FLAG = True

    while (True):        

        _list = []
        _list.append({"link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670846?format=json", "mlb": False})
        _list.append({"link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670846/categories/487/subcategories/4606?format=json", "mlb": False})
        try:        
            pool = ThreadPool(5)
            pool.starmap(draftkings_scrape_market, zip(_list))
            pool.close()
            pool.join()
            # for item in _list:
            #     draftkings_scrape_market(item)

        except Exception as f:
            pass

    M_DRAFT_NBA_FLAG = False

M_DRAFT_NFL_FLAG = False

@shared_task
def get_draftkings_market_nfl():
    global M_DRAFT_NFL_FLAG
    if M_DRAFT_NFL_FLAG == True:
        return

    M_DRAFT_NFL_FLAG = True
    while (True):
        print("start.................", datetime.now())
            
        _list = []
        _list.append({"link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670561?format=json", "mlb": False})
        _list.append({"link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670561/categories/492/subcategories/9909?format=json", "mlb": False})
        try:        
            pool = ThreadPool(5)
            pool.starmap(draftkings_scrape_market, zip(_list))
            pool.close()
            pool.join()

            # for item in _list:
            #     print("save.................", datetime.now())
            #     draftkings_scrape_market(item)
        except Exception as f:
            pass

        print("end.................", datetime.now())

    M_DRAFT_NFL_FLAG = False

M_DRAFT_NHL_FLAG = False

@shared_task
def get_draftkings_market_nhl():
    global M_DRAFT_NHL_FLAG

    _list = []
    _list.append({"link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670853?format=json", "mlb": False})
    _list.append({"link": f"https://sportsbook.draftkings.com//sites/US-SB/api/v4/eventgroups/88670853/categories/496/subcategories/5680?format=json", "mlb": False})
    
    if M_DRAFT_NHL_FLAG == True:
        return

    M_DRAFT_NHL_FLAG = True
    
    while (True):        
        try:            
            # start = time.time()            

            pool = ThreadPool(5)
            pool.starmap(draftkings_scrape_market, zip(_list))            
            pool.close()
            pool.join()
            
            # end = time.time()
            # print('Time taken in seconds -', end - start)
        except Exception as f:
            pass    

    M_DRAFT_NHL_FLAG = False
# fanduel
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
                            market_type = MarketType.TOTAL
                        elif market_type == "Moneyline":
                            market_type = MarketType.MONEYLINE
                        elif market_type == "Spread Betting" or market_type == "Spread" or market_type == 'Puck Line':
                            market_type = MarketType.SPREAD
                        elif market_type == "Alternative Spreads" or market_type == "Alternate Spread" or 'Alternate Spread' in market['marketName']:
                            market_type = MarketType.ALTERNATIVE_SPREAD

                        elif mlb == False:                                
                            continue

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
                pass
        
        print(data["link"], len(selectionInfo))
        saveSelectionInfo(selectionInfo)
    except:
        pass

M_FANDUEL_MLB_FLAG = False
# fanduel
@shared_task
def get_fanduel_market_mlb():
    global M_FANDUEL_MLB_FLAG
    if M_FANDUEL_MLB_FLAG == True:
        return

    M_FANDUEL_MLB_FLAG = True

    while (True):
        try:
            _list = []

            _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId=31248261"
            _list.append({"link": _api,"mlb": True})
                    
            try:        
                pool = ThreadPool(1)
                pool.starmap(fanduel_scrape_market, zip(_list))
                pool.close()
                pool.join()

                # for item in _list:
                #     fanduel_scrape_market(item)
                    
            except Exception as f:
                pass
        except:
            pass    

    M_FANDUEL_MLB_FLAG = False

M_FANDUEL_NBA_FLAG = False    

@shared_task
def get_fanduel_market_nba():
    global M_FANDUEL_NBA_FLAG
    if M_FANDUEL_NBA_FLAG == True:
        return

    M_FANDUEL_NBA_FLAG = True

    while (True):

        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz))
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                for market in item["target_bookies"]:
                    if market["bookie"] == Bookie.FANDUEL:

                        _api = None

                        if item["league"] == League.NBA:
                            _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId={market['self_event_id']}"

                        if _api is not None:
                            _list.append({
                                "link": _api,
                                "mlb": False
                            })  
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(fanduel_scrape_market, zip(_list))
                pool.close()
                pool.join()
                # for item in _list:
                #     fanduel_scrape_market(item)
                    
            except Exception as f:            
                pass
        except:
            pass

    M_FANDUEL_NBA_FLAG = False

M_FANDUEL_NFL_FLAG = False    
@shared_task
def get_fanduel_market_nfl():
    global M_FANDUEL_NFL_FLAG
    if M_FANDUEL_NFL_FLAG == True:
        return
    M_FANDUEL_NFL_FLAG = True

    while (True):
        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz))
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                for market in item["target_bookies"]:
                    if market["bookie"] == Bookie.FANDUEL:

                        _api = None

                        if item["league"] == League.NFL:
                            _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId={market['self_event_id']}"

                        if _api is not None:
                            _list.append({
                                "link": _api,
                                "mlb": False
                            })  
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(fanduel_scrape_market, zip(_list))
                pool.close()
                pool.join()
                # for item in _list:
                #     fanduel_scrape_market(item)
                    
            except Exception as f:            
                pass
        except:
            pass

    M_FANDUEL_NFL_FLAG = False

M_FANDUEL_NHL_FLAG = False
@shared_task
def get_fanduel_market_nhl():
    global M_FANDUEL_NHL_FLAG
    if M_FANDUEL_NHL_FLAG == True:
        return

    M_FANDUEL_NHL_FLAG = True
    while (True):
        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz))
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                for market in item["target_bookies"]:
                    if market["bookie"] == Bookie.FANDUEL:

                        _api = None

                        if item["league"] == League.NHL:
                            _api = f"https://sbapi.nj.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId={market['self_event_id']}"

                        if _api is not None:
                            _list.append({
                                "link": _api,
                                "mlb": False
                            })  
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(fanduel_scrape_market, zip(_list))
                pool.close()
                pool.join()
                # for item in _list:
                #     fanduel_scrape_market(item)
                    
            except Exception as f:            
                pass
        except:
            pass    
    M_FANDUEL_NHL_FLAG = False
    
# get the market from result string
def twinspires_scrape_market(data):
    try:
        _api = data["link"]
        mlb = data["mlb"]        

        session = requests.Session()
        response = session.request("GET", _api)
        result = json.loads(response.text.encode('utf8'))

        selectionInfo = []

        # marketNameList = ['Point Spread', 'Total Points', 'Moneyline', 'Alternative Spreads']

        marketNameList = []
        for market in result['betOffers']:
            for selection in market["outcomes"]:
                if "MAIN_LINE" in market["tags"] or "MAIN" in market["tags"]:
                    if market["criterion"]["label"] not in marketNameList:
                        marketNameList.append(market["criterion"]["label"])                        

        for market in result['betOffers']:
            try:
                for selection in market["outcomes"]:
                    if (market["criterion"]["label"] == "Total Points" or market["criterion"]["label"] == 'Total Goals - Inc. OT and Shootout' or market["criterion"]["label"] == 'Total Goals') and ("MAIN_LINE" not in market["tags"] and "MAIN" not in market["tags"]):                            
                        continue
                    
                    market_type = market["criterion"]["label"]

                    if (market_type == "Point Spread" or market_type == "Puck Line - Inc. OT and Shootout" or market_type == 'Puck Line') and ("MAIN_LINE" not in market["tags"] or "MAIN" in market["tags"]):
                        market_type = "Alternative Spreads"

                    if (market_type == "Point Spread" or market_type == "Puck Line - Inc. OT and Shootout" or market_type == 'Puck Line') and ("MAIN_LINE" in market["tags"] or "MAIN" in market["tags"]):
                        market_type = "Spread"
                    
                    if market["criterion"]["label"] == "Total Points" or market["criterion"]["label"] == 'Total Goals - Inc. OT and Shootout' or market["criterion"]["label"] == 'Total Goals':
                        market_type = MarketType.TOTAL

                    elif market_type == "Moneyline" or market_type == 'Moneyline - Inc. OT and Shootout':
                        market_type = MarketType.MONEYLINE

                    elif market_type == "Spread":
                        market_type = MarketType.SPREAD

                    elif market_type == "Alternative Spreads":
                        market_type = MarketType.ALTERNATIVE_SPREAD

                    elif mlb == False:                                                   
                        continue                                                            

                    marketId = str(market["criterion"]["id"])
                    if market_type == MarketType.SPREAD:
                        marketId = str(marketId) + "_Main"

                    selectionInfo.append({
                        "self_selection_id": selection["id"],
                        "market_type": market_type,
                        "line": getValue(selection, "line", 1000),
                        "name": selection["label"],
                        "eventId": market['eventId'],
                        "self_market_id": marketId, # market["criterion"]["id"],
                        "updateTime": datetime.now(tz),
                        "odds": float(selection["odds"]) / 1000,
                        "oddsAmerican": selection["oddsAmerican"],
                        "self_event_id": market['eventId']
                    })

            except:                
                pass
                        
        saveSelectionInfo(selectionInfo)
    except:
        pass

M_TWINSPIRES_MLB_FLAG = False        
# twinspires
@shared_task
def get_twinspires_market_mlb():
    global M_TWINSPIRES_MLB_FLAG
    if M_TWINSPIRES_MLB_FLAG == True:
        return
    M_TWINSPIRES_MLB_FLAG = True

    while (True):
        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz)).order_by('-league')
            record = Event.objects.order_by('-league')
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                if item["league"] == League.MLB:
                    for market in item["target_bookies"]:
                        if market["bookie"] == Bookie.TWINSPIRES:
                            _api = None
                            _time = int(time.time() *1000)
                            
                            _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/betoffer/event/{market['self_event_id']}.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&includeParticipants=true"

                            if _api is not None:
                                _list.append({
                                    "link": _api,
                                    "mlb": item["league"] == League.MLB
                                })        
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(twinspires_scrape_market, zip(_list))
                pool.close()
                pool.join()

                # for item in _list:
                #     twinspires_scrape_market(item)
                    
            except Exception as f:            
                pass
        except:
            pass

    M_TWINSPIRES_MLB_FLAG = False

M_TWINSPIRES_NBA_FLAG = False    
@shared_task
def get_twinspires_market_nba():
    global M_TWINSPIRES_NBA_FLAG
    if M_TWINSPIRES_NBA_FLAG == True:
        return

    M_TWINSPIRES_NBA_FLAG = True
    while (True):
        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz)).order_by('-league')
            record = Event.objects.order_by('-league')
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                if item["league"] == League.NBA:
                    for market in item["target_bookies"]:
                        if market["bookie"] == Bookie.TWINSPIRES:
                            _api = None
                            _time = int(time.time() *1000)
                            
                            _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/betoffer/event/{market['self_event_id']}.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&includeParticipants=true"

                            if _api is not None:
                                _list.append({
                                    "link": _api,
                                    "mlb": item["league"] == League.MLB
                                })        
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(twinspires_scrape_market, zip(_list))
                pool.close()
                pool.join()
                # for item in _list:
                #     twinspires_scrape_market(item)
                    
            except Exception as f:            
                pass
        except:
            pass    
    M_TWINSPIRES_NBA_FLAG = False

M_TWINSPIRES_NFL_FLAG = False    
@shared_task
def get_twinspires_market_nfl():
    global M_TWINSPIRES_NFL_FLAG
    if M_TWINSPIRES_NFL_FLAG == True:
        return

    M_TWINSPIRES_NFL_FLAG = True

    while (True):
        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz)).order_by('-league')
            record = Event.objects.order_by('-league')
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                if item["league"] == League.NFL:
                    for market in item["target_bookies"]:
                        if market["bookie"] == Bookie.TWINSPIRES:
                            _api = None
                            _time = int(time.time() *1000)
                            
                            _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/betoffer/event/{market['self_event_id']}.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&includeParticipants=true"

                            if _api is not None:
                                _list.append({
                                    "link": _api,
                                    "mlb": item["league"] == League.MLB
                                })        
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(twinspires_scrape_market, zip(_list))
                pool.close()
                pool.join()
                # for item in _list:
                #     twinspires_scrape_market(item)

            except Exception as f:            
                pass
        except:
            pass    
    M_TWINSPIRES_NFL_FLAG = False

M_TWINSPIRES_NHL_FLAG = False

@shared_task
def get_twinspires_market_nhl():
    global M_TWINSPIRES_NHL_FLAG

    if M_TWINSPIRES_NHL_FLAG == True:
        return
    M_TWINSPIRES_NHL_FLAG = True

    while (True):
        try:
            _list = []

            record = Event.objects.filter(startTime__gte=datetime.now(tz)).order_by('-league')
            record = Event.objects.order_by('-league')
            serial = BookieLinkSerializer(record, many=True)
            for item in serial.data:
                if item["league"] == League.NHL:
                    for market in item["target_bookies"]:
                        if market["bookie"] == Bookie.TWINSPIRES:
                            _api = None
                            _time = int(time.time() *1000)
                            
                            _api = f"https://eu-offering.kambicdn.org/offering/v2018/winusco/betoffer/event/{market['self_event_id']}.json?lang=en_US&market=US-CO&client_id=2&channel_id=1&ncid={_time}&includeParticipants=true"

                            if _api is not None:
                                _list.append({
                                    "link": _api,
                                    "mlb": item["league"] == League.MLB
                                })        
            
            try:        
                pool = ThreadPool(5)
                pool.starmap(twinspires_scrape_market, zip(_list))
                pool.close()
                pool.join()
                # for item in _list:
                #     twinspires_scrape_market(item)

            except Exception as f:            
                pass
        except:
            pass       
    M_TWINSPIRES_NHL_FLAG = False