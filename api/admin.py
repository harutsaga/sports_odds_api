from django.contrib import admin
from .models import *

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('sports', 'league', 'name', 'startTime', 'updateTime', 'awayName', 'homeName', 'e_id', 'full_name')

@admin.register(BookieEvent)
class BookieEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'self_event_id', 'bookie')

@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'updateTime', 'odds', 'oddsAmerican', 'line', 'self_selection_id', 'self_market_id', 'self_event_id')

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('self_market_id', 'market_type', 'self_event_id')
