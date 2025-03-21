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
        fields = [
            'player_id',
            'team_id',
            'jersey_number',
            'name',
            'isForeign',
            'isRookie',
            'wasAbroad',
            'pitching_hand',
            'batting_hand',
            'main_pos',
            'batting_games',
            'batting_appearances',
            'pitching_games',
            'pitching_innings3',
            'is_injured',
            'sp_games',
            'rp_games',
            'c_games',
            '_1b_games',
            '_2b_games',
            '_3b_games',
            'ss_games',
            'of_games',
            'lf_games',
            'cf_games',
            'rf_games',
            'mvp_counts',
            'stats',  # ✅ 內嵌 stats
        ]
