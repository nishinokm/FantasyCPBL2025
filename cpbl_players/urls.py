from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CPBLPlayerViewSet, player_search_api

router = DefaultRouter()
router.register(r'players', CPBLPlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
     path('api/search/', player_search_api, name='player_search_api'),
]