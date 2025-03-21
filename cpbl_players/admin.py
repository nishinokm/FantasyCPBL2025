from django.contrib import admin
from .models import CPBLPlayer, CPBLPlayerStats

# Inline：讓你在 CPBLPlayer 裡面直接編輯 stats
class CPBLPlayerStatsInline(admin.StackedInline):
    model = CPBLPlayerStats
    extra = 0
    max_num = 1
    can_delete = False

@admin.register(CPBLPlayer)
class CPBLPlayerAdmin(admin.ModelAdmin):
    list_display = (
        'player_id', 'name', 'team_id', 'jersey_number',
        'isForeign', 'main_pos', 'batting_games', 'pitching_games', 'is_injured'
    )
    list_filter = ('isForeign', 'is_injured', 'main_pos')
    search_fields = ('name', 'jersey_number', 'player_id')
    ordering = ('player_id',)
    inlines = [CPBLPlayerStatsInline]

@admin.register(CPBLPlayerStats)
class CPBLPlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'games_played', 'hits', 'home_runs', 'rbi')
    list_filter = ('year',)
    search_fields = ('player__name',)