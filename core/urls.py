# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import set_language

try:
    from rest_framework.authtoken.views import obtain_auth_token
except:
    pass

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("admin_material.urls")),
    path('i18n/setlang/', set_language, name='set_language'),
    path('leagues/', include('fb_leagues.urls')),
    path('api/', include('cpbl_players.urls')),
    path('draft/', include('draft.urls')),
    path('players/', include('cpbl_players.urls')),
]


# Lazy-load on routing is needed
# During the first build, API is not yet generated
try:
    urlpatterns.append(path("", include("django_dyn_api.urls")))
    urlpatterns.append(path("login/jwt/", view=obtain_auth_token))
except:
    pass
