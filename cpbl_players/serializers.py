from rest_framework import serializers
from .models import CPBLPlayer, CPBLPlayerStats, CPBLPlayerBoxPitcher, CPBLPlayerBoxBatter

class CPBLPlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPBLPlayerStats
        fields = '__all__'

class CPBLPlayerSerializer(serializers.ModelSerializer):
    stats = CPBLPlayerStatsSerializer(read_only=True)

    class Meta:
        model = CPBLPlayer
        fields = '__all__'

class CPBLPlayerBoxPitcherSerializer(serializers.ModelSerializer):
    player = CPBLPlayerSerializer(read_only=True)

    class Meta:
        model = CPBLPlayerBoxPitcher
        fields = '__all__'

class CPBLPlayerBoxBatterSerializer(serializers.ModelSerializer):
    player = CPBLPlayerSerializer(read_only=True)

    class Meta:
        model = CPBLPlayerBoxBatter
        fields = '__all__'