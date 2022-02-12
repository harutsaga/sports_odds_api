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
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(operation_description="Get all supported bookies.", operation_id='get_bookies', responses={200: openapi.Response('Bookie names', schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)))})
    def get(self, request):
        _list = []
        for item in Bookie.choices:
            _list.append(item[0])
        return Response(_list, status=status.HTTP_200_OK)

class SportsView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(operation_description="Get all supported sports types.", operation_id='get_sports', responses={200: openapi.Response('Sports type names', schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)))})
    def get(self, request):
        _list = []
        for item in SportsType.choices:
            _list.append(item[0])
        return Response(_list, status=status.HTTP_200_OK)
        

class MarketView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(operation_description="Get all supported market types.", operation_id='get_markets', responses={200: openapi.Response('Market type names', schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)))})
    def get(self, request):
        _list = []
        for item in MarketType.choices:
            _list.append(item[0])
        return Response(_list, status=status.HTTP_200_OK)

class EventView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.filter(startTime__gte=datetime.utcnow()).order_by('-startTime')

class SelectionView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BookieLinkSerializer
    queryset = Event.objects.filter(startTime__gte=datetime.utcnow()).order_by('-league')