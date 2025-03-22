from rest_framework import viewsets, filters
from .models import CPBLPlayer
from .serializers import CPBLPlayerSerializer
from django.http import JsonResponse
from django.db.models import Q

class CPBLPlayerViewSet(viewsets.ModelViewSet):
    queryset = CPBLPlayer.objects.all().order_by('player_id')
    serializer_class = CPBLPlayerSerializer
    lookup_field = 'player_id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

def player_search_api(request):
    query = request.GET.get("q", "")
    players = CPBLPlayer.objects.filter(Q(name__icontains=query))[:20]
    results = [
        {"id": p.id, "text": f"{p.name}（#{p.jersey_number}）"} for p in players
    ]
    return JsonResponse({"results": results})