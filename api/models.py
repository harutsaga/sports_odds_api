from django.db import models
from datetime import datetime   
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Bookie(models.TextChoices):
    DRAFTKING = 'Draft Kings', _('Draft Kings')
    FANDUEL = 'Fanduel', _('Fanduel')
    TWINSPIRES = 'TwinSpires', _('TwinSpires')    

class SportsType(models.TextChoices):
    BASKETBALL = 'Basketball', _('Basketball')
    BASEBALL = 'Baseball', _('Baseball')
    ICE_HOCKEY = 'Ice Hockey', _('Ice Hockey')
    FOOTBALL = 'Football', _('Football')

class League(models.TextChoices):
    NBA = 'NBA', _('NBA')   #National Basketball Association
    MLB = 'MLB', _('MLB')   #Major League of Baseball
    NHL = 'NHL', _('NHL')   #Mational Hockey League
    NFL = 'NFL', _('NFL')    #National Football League

class MarketType(models.TextChoices):
    SPREAD = 'Spread', _('Spread')
    TOTAL = 'Total', _('Total Points')
    MONEYLINE = 'Money Line', _('Money line')
    ALTERNATIVE_SPREAD = 'Alternative Spreads', _('Alternative Spreads')

class Event(models.Model):
    sports = models.CharField(max_length=255, choices=SportsType.choices, default=SportsType.BASKETBALL, db_index=True)
    league = models.CharField(max_length=255, choices=League.choices, default=League.NBA, db_index=True)
    # name of the event
    name = models.CharField(max_length=255, db_index=True)  #Metropolitan Division @ Atlantic Division
    # start time
    startTime = models.DateTimeField(null=True, blank=True, db_index=True)
    # update time
    updateTime = models.DateTimeField(null=True, blank=True)
    # away
    awayName = models.CharField(max_length=255, null=True, blank=True, db_index=True)  #Metropolitan Division
    # home
    homeName = models.CharField(max_length=255, null=True, blank=True, db_index=True)  #Atlantic Division
    # event id
    e_id = models.CharField(max_length=255, null=True, db_index=True)
    # english name
    english_name = models.CharField(max_length=255, null=True, db_index=True)

    def __str__(self):
        return f'{self.sports} - {self.league} - {self.name}'

class BookieEvent(models.Model):    
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='event', null=True)
    self_event_id = models.CharField(max_length=255, db_index=True)    
    bookie = models.CharField(max_length=255, choices=Bookie.choices, default=Bookie.TWINSPIRES)

class Selection(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    odds = models.FloatField(default=1, null=True)
    oddsAmerican = models.FloatField(default=1, null=True)
    line = models.CharField(max_length=255, null=True, blank=True)
    self_selection_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    self_market_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    updateTime = models.DateTimeField(null=True, blank=True)
    self_event_id = models.CharField(max_length=255, db_index=True, null=True)   
    
class Market(models.Model):
    self_market_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    market_type = models.CharField(max_length=255, choices=MarketType.choices, default=MarketType.SPREAD)
    selection = models.ManyToManyField(Selection, blank=True)    
    self_event_id = models.CharField(max_length=255, db_index=True, null=True)   