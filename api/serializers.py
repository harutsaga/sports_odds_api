from rest_framework import serializers
from django.contrib import auth
from django.db import models
from django.db. models import Q
from .models import Event, BookieEvent, Selection, Market

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['name', 'odds', 'oddsAmerican', 'line', 'updateTime']

class MarketSerializer(serializers.ModelSerializer):
    selection = SelectionSerializer(read_only=True, many=True)

    class Meta:
        model = Market
        fields = ['market_type', 'selection']

class BookieEventSerializer(serializers.ModelSerializer):

    market = serializers.SerializerMethodField()

    class Meta:
        model = BookieEvent
        fields = ['self_event_id', 'bookie', 'market']

    def get_market(self, obj):
        try:            
            c = Market.objects.filter(self_event_id=obj.self_event_id).count()            
            serial = MarketSerializer(Market.objects.filter(self_event_id=obj.self_event_id), many=True)            
            return list(serial.data)
        except:
            pass

class BookieLinkSerializer(serializers.ModelSerializer):
    
    target_bookies = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'sports', 'league', 'name', 'startTime', 'updateTime', 'awayName', 'homeName', 'full_name', 'target_bookies']

    def get_target_bookies(self, obj):
        try:            
            serial = BookieEventSerializer(BookieEvent.objects.filter(event__id=obj.id), many=True)
            return list(serial.data)
        except:
            return []