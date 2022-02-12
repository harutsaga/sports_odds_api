from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import api

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),    
    path('', include('api.urls'))
]


# open api, disable on production mode
schema_view = get_schema_view(
    openapi.Info(
        title="Sports Odds API",
        default_version='v1',
        description="Documentation of API for Sports Odds Integration v1."),
    public=True,
    permission_classes=[],
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    re_path(r'^.*$', api.views.index),    
]