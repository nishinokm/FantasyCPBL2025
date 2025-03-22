from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CPBLPlayerViewSet, player_search_api, CPBLPlayerBoxPitcherViewSet, CPBLPlayerBoxBatterViewSet

router = DefaultRouter()
router.register(r'players', CPBLPlayerViewSet)
router.register(r'box_pitchers', CPBLPlayerBoxPitcherViewSet, basename='box-pitcher')
router.register(r'box_batters', CPBLPlayerBoxBatterViewSet, basename='box-batter')
urlpatterns = [
    path('', include(router.urls)),
    path('api/search/', player_search_api, name='player_search_api'),
]