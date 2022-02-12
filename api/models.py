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
    NBA = 'NBA', _('NBA')  # National Basketball Association
    MLB = 'MLB', _('MLB')  # Major League of Baseball
    NHL = 'NHL', _('NHL')  # Mational Hockey League
    NFL = 'NFL', _('NFL')  # National Football League


class MarketType(models.TextChoices):
    SPREAD = 'Spread', _('Spread')
    TOTAL = 'Total', _('Total Points')
    MONEYLINE = 'Money Line', _('Money line')
    ALTERNATIVE_SPREAD = 'Alternative Spreads', _('Alternative Spreads')


class Event(models.Model):
    sports = models.CharField(max_length=255, choices=SportsType.choices,
                              default=SportsType.BASKETBALL, db_index=True, help_text=_('Sports'))
    league = models.CharField(max_length=255, choices=League.choices, default=League.NBA,
                              db_index=True, help_text=_('League'))
    # name of the event
    name = models.CharField(max_length=255, db_index=True, help_text=_('Name of the event. e.g., Metropolitan Division @ Atlantic Division')
                            )  # Metropolitan Division @ Atlantic Division
    # start time
    startTime = models.DateTimeField(null=True, blank=True, db_index=True, help_text=_('Start time of the event'))
    # update time
    updateTime = models.DateTimeField(null=True, blank=True, help_text=_('Updated time'))
    # away
    awayName = models.CharField(max_length=255, null=True, blank=True, db_index=True,
                                help_text=_('Away team name'))  # Metropolitan Division
    # home
    homeName = models.CharField(max_length=255, null=True, blank=True, db_index=True,
                                help_text=_('Home team name'))  # Atlantic Division
    # event id
    e_id = models.CharField(max_length=255, null=True, db_index=True, help_text=_('ID of the event'))

    # english name
    english_name = models.CharField(max_length=255, null=True, db_index=True, help_text=_('Name of the event'))

    def __str__(self):
        return f'{self.sports} - {self.league} - {self.name}'


class BookieEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='event', null=True, help_text=_('Event')) # ? add example
    self_event_id = models.CharField(max_length=255, db_index=True, help_text=_('Event ID')) # ? add example
    bookie = models.CharField(max_length=255, choices=Bookie.choices, default=Bookie.TWINSPIRES, help_text=_('Bookie')) # ? add example


class Selection(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text=_('Name of the selection'))
    updateTime = models.DateTimeField(null=True, blank=True, help_text=_('Update time'))
    odds = models.FloatField(default=1, null=True, help_text=_('Odds for this selection'))
    oddsAmerican = models.FloatField(default=1, null=True, help_text=_('American odds for this selection'))
    line = models.CharField(max_length=255, null=True, blank=True, help_text=_('Line of the selection')) # ? add example
    self_selection_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text=_('self selection id'))# ? add example
    self_market_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text=_('self market id'))# ? add example
    self_event_id = models.CharField(max_length=255, db_index=True, null=True, help_text=_('self event id'))


class Market(models.Model):
    self_market_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text=_('self market id'))# ? add example
    market_type = models.CharField(max_length=255, choices=MarketType.choices, default=MarketType.SPREAD, help_text=_('Market type'))# ? add example
    selection = models.ManyToManyField(Selection, blank=True, help_text=_('Selections for this market'))
    self_event_id = models.CharField(max_length=255, db_index=True, null=True, help_text=_('Events for this market'))
