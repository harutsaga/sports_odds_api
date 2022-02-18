from celery.schedules import crontab
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'scrape_base_event': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_base_event'
    },
    'scrape_bookie_event': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_bookie_event'
    },
    'fanduel_nhl': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_fanduel_market_nhl'
    },
    'fanduel_nfl': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_fanduel_market_nfl'
    },
    'fanduel_nba': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_fanduel_market_nba'
    },
    'fanduel_mlb': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_fanduel_market_mlb'
    },
    'draftking_nhl': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_draftkings_market_nhl'
    },
    'draftking_nfl': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_draftkings_market_nfl'
    },
    'draftking_nba': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_draftkings_market_nba'
    },
    'draftking_mlb': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_draftkings_market_mlb'
    },
    'twinspires_nhl': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_twinspires_market_nhl'
    },
    'twinspires_nfl': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_twinspires_market_nfl'
    },
    'twinspires_nba': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_twinspires_market_nba'
    },
    'twinspires_mlb': {
        'schedule': timedelta(minutes=1),
        'task': 'api.tasks.get_twinspires_market_mlb'
    },
}
