from rest_framework import viewsets, filters
from .models import CPBLPlayer, CPBLPlayerBoxPitcher, CPBLPlayerBoxBatter
from .serializers import CPBLPlayerSerializer, CPBLPlayerBoxPitcherSerializer, CPBLPlayerBoxBatterSerializer
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

class CPBLPlayerBoxPitcherViewSet(viewsets.ModelViewSet):
    queryset = CPBLPlayerBoxPitcher.objects.select_related('player').order_by('-date')
    serializer_class = CPBLPlayerBoxPitcherSerializer
    filterset_fields = ['date', 'pitcher_name', 'player__id']
    filter_backends = [filters.SearchFilter]
    search_fields = ['pitcher_name', 'pitcher_uniform_no', 'player__name']

    def perform_create(self, serializer):
        name = serializer.validated_data.get('pitcher_name', '').strip().replace('　', '').replace(' ', '')
        jersey = serializer.validated_data.get('pitcher_uniform_no', '').strip()

        players = CPBLPlayer.objects.all()
        matched_player = next((
            p for p in players
            if p.name.replace('　', '').replace(' ', '') == name and p.jersey_number == jersey
        ), None)

        serializer.save(player=matched_player)

class CPBLPlayerBoxBatterViewSet(viewsets.ModelViewSet):
    queryset = CPBLPlayerBoxBatter.objects.select_related('player').order_by('-date')
    serializer_class = CPBLPlayerBoxBatterSerializer
    filterset_fields = ['date', 'hitter_name', 'player__id']
    filter_backends = [filters.SearchFilter]
    search_fields = ['hitter_name', 'hitter_uniform_no', 'player__name']

    def perform_create(self, serializer):
        name = serializer.validated_data.get('hitter_name', '').strip().replace('　', '').replace(' ', '')
        jersey = serializer.validated_data.get('hitter_uniform_no', '').strip()

        players = CPBLPlayer.objects.all()
        matched_player = next((
            p for p in players
            if p.name.replace('　', '').replace(' ', '') == name and p.jersey_number == jersey
        ), None)

        serializer.save(player=matched_player)