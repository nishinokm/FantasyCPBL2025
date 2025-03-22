from django.contrib import admin
from .models import RankingRecord, RankingPitcherDetail, RankingBatterDetail

@admin.register(RankingRecord)
class RankingRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank_type', 'year', 'start_date', 'end_date', 'author', 'created_at')
    list_filter = ('rank_type', 'year', 'start_date', 'end_date')
    search_fields = ('remark', 'author__username')
    ordering = ('-year', '-start_date')
    date_hierarchy = 'start_date'

@admin.register(RankingPitcherDetail)
class RankingPitcherDetailAdmin(admin.ModelAdmin):
    list_display = ('ranking_record', 'player', 'ranking', 'ip', 'era', 'fip', 'mvp')
    list_filter = ('ranking_record__year', 'ranking_record__rank_type')
    search_fields = ('player__name', 'ranking_record__remark')
    ordering = ('ranking_record__year', 'ranking', '-ip')

@admin.register(RankingBatterDetail)
class RankingBatterDetailAdmin(admin.ModelAdmin):
    list_display = ('ranking_record', 'player', 'ranking', 'rrbi', 'avg', 'obp', 'isop', 'mvp')
    list_filter = ('ranking_record__year', 'ranking_record__rank_type')
    search_fields = ('player__name', 'ranking_record__remark')
    ordering = ('ranking_record__year', 'ranking', '-rrbi')