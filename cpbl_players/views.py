from rest_framework import viewsets, filters
from .models import CPBLPlayer
from .serializers import CPBLPlayerSerializer

class CPBLPlayerViewSet(viewsets.ModelViewSet):
    queryset = CPBLPlayer.objects.all().order_by('player_id')
    serializer_class = CPBLPlayerSerializer
    lookup_field = 'player_id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']