from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CPBLPlayerViewSet

router = DefaultRouter()
router.register(r'players', CPBLPlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]