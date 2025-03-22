from django.contrib import admin
from .models import CPBLPlayer, CPBLPlayerStats, CPBLPlayerBoxPitcher, CPBLPlayerBoxBatter

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
        'isForeign','isRookie','wasAbroad', 'main_pos', 'batting_games','batting_appearances', 'pitching_games','pitching_innings3', 'is_injured'
    )
    list_filter = ('isForeign','isRookie','wasAbroad', 'is_injured', 'main_pos')
    search_fields = ('name', 'jersey_number', 'player_id')
    ordering = ('player_id',)
    inlines = [CPBLPlayerStatsInline]

@admin.register(CPBLPlayerStats)
class CPBLPlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'games_played', 'hits', 'home_runs', 'rbi')
    list_filter = ('year',)
    search_fields = ('player__name',)

@admin.register(CPBLPlayerBoxPitcher)
class CPBLPlayerBoxPitcherAdmin(admin.ModelAdmin):
    list_display = ('pitcher_name', 'pitcher_uniform_no','year','game_sno', 'date', 'player')
    search_fields = ('pitcher_name', 'pitcher_uniform_no', 'player__name','year','game_sno')
    list_filter = ('role', 'date')
    autocomplete_fields = ['player']

@admin.register(CPBLPlayerBoxBatter)
class CPBLPlayerBoxBatterAdmin(admin.ModelAdmin):
    list_display = ('hitter_name', 'hitter_uniform_no','year','game_sno', 'date', 'player')
    search_fields = ('hitter_name', 'hitter_uniform_no', 'player__name','year','game_sno')
    list_filter = ('date',)
    autocomplete_fields = ['player']