
from django.contrib import admin
from .models import DraftRoom, DraftUnit

class DraftUnitInline(admin.TabularInline):
    model = DraftUnit
    extra = 0
    fields = ('round', 'pick', 'ori_owner', 'new_owner', 'player', 'pre_draft', 'pick_at_time')
    readonly_fields = ('pick_at_time',)
    ordering = ('round', 'pick')

@admin.register(DraftRoom)
class DraftRoomAdmin(admin.ModelAdmin):
    list_display = ('league', 'draft_type', 'current_round', 'current_pick', 'is_complete', 'started_at')
    list_filter = ('draft_type', 'is_complete')
    search_fields = ('league__name',)
    inlines = [DraftUnitInline]
    ordering = ('-started_at',)
    readonly_fields = ('started_at',)

@admin.register(DraftUnit)
class DraftUnitAdmin(admin.ModelAdmin):
    list_display = ('draft', 'round', 'pick', 'ori_owner', 'new_owner', 'player', 'pre_draft', 'pick_at_time')
    list_filter = ('round', 'pre_draft')
    search_fields = ('player__name', 'ori_owner__name', 'new_owner__name')
    ordering = ('draft', 'round', 'pick')