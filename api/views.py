from datetime import date, datetime, timedelta, timezone
from multiprocessing.dummy import Pool as ThreadPool

from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import (Bookie, BookieEvent, Event, League, Market, MarketType,
                        Selection, SportsType)
from api.serializers import (BookieEventSerializer, BookieLinkSerializer,
                             EventSerializer)


def index(request):
    return render(request, 'index.html')

class BookieView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(operation_description="Get all supported bookies.", operation_id='get_bookies', responses={200: openapi.Response('Bookie names', schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)))})
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
