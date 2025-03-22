from rest_framework import serializers
from .models import CPBLPlayer, CPBLPlayerStats

class CPBLPlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPBLPlayerStats
        fields = ['year', 'games_played', 'hits', 'home_runs', 'rbi']

class CPBLPlayerSerializer(serializers.ModelSerializer):
    stats = CPBLPlayerStatsSerializer(read_only=True)

    class Meta:
        model = CPBLPlayer
        fields = '__all__'
