from rest_framework import serializers
from .models import League, LeagueConfig, LeagueMembership, FantasyTeam, FantasyPlayer

class LeagueConfigSerializer(serializers.ModelSerializer):
    max_rosters = serializers.ReadOnlyField()
    max_pitcher_num = serializers.ReadOnlyField()
    max_players = serializers.ReadOnlyField()
    class Meta:
        model = LeagueConfig
        exclude = ['league']  # league 是由 LeagueSerializer 自動設置，不讓使用者手動傳

class LeagueSerializer(serializers.ModelSerializer):
    config = LeagueConfigSerializer()

    class Meta:
        model = League
        fields = ['league_id', 'name', 'created_by', 'config']

    def create(self, validated_data):
        config_data = validated_data.pop('config')
        league = League.objects.create(**validated_data)
        LeagueConfig.objects.create(league=league, **config_data)
        return league

    def update(self, instance, validated_data):
        config_data = validated_data.pop('config', None)

        if config_data:
            config = instance.config
            for attr, value in config_data.items():
                setattr(config, attr, value)
            config.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance