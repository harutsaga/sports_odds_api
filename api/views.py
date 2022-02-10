from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import HttpResponse
import json
from datetime import datetime, timedelta, timezone
from django.contrib import auth
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import render
import pytz
from django.conf import settings
from django.db import connection
from api.models import Event, Selection, Market, BookieEvent, SportsType, League, MarketType, Bookie
from api.serializers import EventSerializer, BookieEventSerializer, BookieLinkSerializer
import requests
import json
import traceback
from multiprocessing.dummy import Pool as ThreadPool 
import traceback
import time
from dateutil import parser, tz
from datetime import datetime, date, timedelta     

def index(request):
    return render(request, 'index.html')

class BookieView(APIView):
    def get(self, request):

        _list = []
        for item in Bookie.choices:
            _list.append(item[0])
        return Response(_list, status=status.HTTP_200_OK)

class SportsView(APIView):
    def get(self, request):
        _list = []
        for item in SportsType.choices:
            _list.append(item[0])
        return Response(_list, status=status.HTTP_200_OK)
        
class EventView(APIView):
    def get(self, request):
        record = Event.objects.filter(startTime__gte=datetime.utcnow()).order_by('-startTime')
        # record = Event.objects.filter(league=League.MLB).order_by('-league')
        serial = EventSerializer(record, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)

class MarketView(APIView):
    def get(self, request):
        _list = []
        for item in MarketType.choices:
            _list.append(item[0])
        return Response(_list, status=status.HTTP_200_OK)

class SelectionView(APIView):
    def get(self, request):
        record = Event.objects.filter(startTime__gte=datetime.utcnow()).order_by('-league')
        # record = Event.objects.filter(league=League.MLB).order_by('-league')
        serial = BookieLinkSerializer(record, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)