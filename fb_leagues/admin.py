from django.contrib import admin, messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.urls import path, reverse
from django import forms
from .models import League, LeagueConfig, LeagueMembership, FantasyTeam, FantasyPlayer

class FantasyTeamForm(forms.ModelForm):
    class Meta:
        model = FantasyTeam
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

# 讓 LeagueConfig 在 LeagueAdmin 中直接嵌入建立
class LeagueConfigInline(admin.StackedInline):
    model = LeagueConfig
    extra = 0
    max_num = 1
    can_delete = False

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_id', 'name', 'created_by', 'is_public','has_draft')
    list_filter = ('is_public',)
    inlines = [LeagueConfigInline]
    raw_id_fields = ('created_by',)
    readonly_fields = ('invite_links', 'refresh_button')

    fieldsets = (
        (None, {
            'fields': ('name', 'created_by', 'is_public', 'has_draft')
        }),
        ("邀請功能", {
            'fields': ('invite_links', 'refresh_button')
        }),
    )

    # 當第一次儲存聯盟時，自動產生 token
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # 只有在 "add" 時執行
            obj.generate_invite_tokens()
        if not hasattr(obj, 'config'):
            LeagueConfig.objects.create(league=obj)

    # 顯示邀請連結
    def invite_links(self, obj):
        if not obj.pk:
            return "儲存後將自動產生邀請連結"
        return format_html(
            """
            <div>
                <b>Mod：</b><a href="/leagues/invite/{0}/" target="_blank">{0}</a><br>
                <b>Player：</b><a href="/leagues/invite/{1}/" target="_blank">{1}</a><br>
                <b>Viewer：</b><a href="/leagues/invite/{2}/" target="_blank">{2}</a>
            </div>
            """,
            obj.invite_token_mod or "(尚未產生)",
            obj.invite_token_player or "(尚未產生)",
            obj.invite_token_viewer or "(尚未產生)"
        )
    invite_links.short_description = "邀請連結"

    # 顯示刷新按鈕（僅在已存在的 league 上顯示）
    def refresh_button(self, obj):
        if not obj.pk:
            return "儲存後才能重新產生邀請碼"
        url = reverse('admin:fb_leagues_league_refresh_invites', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="padding: 6px 12px; background:#198754; color:white; border-radius:5px;">重新產生邀請碼</a>',
            url
        )
    refresh_button.short_description = "操作"

    # 自訂刷新按鈕的 URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:league_id>/refresh-invites/',
                self.admin_site.admin_view(self.refresh_invites),
                name='fb_leagues_league_refresh_invites'
            ),
        ]
        return custom_urls + urls

    def refresh_invites(self, request, league_id):
        league = get_object_or_404(League, pk=league_id)
        league.generate_invite_tokens()
        self.message_user(request, f"成功為「{league.name}」重新產生邀請碼")
        return redirect(reverse('admin:fb_leagues_league_change', args=[league_id]))

@admin.register(LeagueMembership)
class LeagueMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'league', 'role', 'joined_at')
    list_filter = ('role',)
    raw_id_fields = ('user', 'league')

class FantasyPlayerInline(admin.TabularInline):
    model = FantasyPlayer
    extra = 1

@admin.register(FantasyTeam)
class FantasyTeamAdmin(admin.ModelAdmin):
    form = FantasyTeamForm
    list_display = ('name', 'league', 'owner', 'color_display')
    list_filter = ('league',)

    def color_display(self, obj):
        return format_html('<div style="width: 30px; height: 20px; background-color: {};"></div>', obj.color)
    color_display.short_description = "顏色"

@admin.register(FantasyPlayer)
class FantasyPlayerAdmin(admin.ModelAdmin):
    list_display = ('team', 'cpbl_player')
    raw_id_fields = ('team', 'cpbl_player')
