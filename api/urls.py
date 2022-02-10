from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from api import views
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = static(settings.CSS_URL, document_root=settings.CSS_ROOT) + [        
    path('api/bookies', views.BookieView.as_view()), 
    path('api/sports', views.SportsView.as_view()),
    path('api/event', views.EventView.as_view()),
    path('api/selection', views.SelectionView.as_view()),            
    path('api/market', views.MarketView.as_view()),    
    re_path(r'^.*$', views.index),    
] 

urlpatterns = format_suffix_patterns(urlpatterns)

