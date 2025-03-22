# leagues/models.py
from django.db import models
from django.conf import settings
from cpbl_players.models import CPBLPlayer
import secrets
from django.core.exceptions import ValidationError

LEAGUE_ROLE_CHOICES = [
    ('owner', 'Owner'),
    ('mod', 'Moderator'),
    ('player', 'Player'),
    ('viewer', 'Viewer'),
]
class LeagueConfig(models.Model):
    league = models.OneToOneField('League', on_delete=models.CASCADE, related_name='config')
    config_name = models.CharField(max_length=100, default='預設配置')
    max_players = models.PositiveIntegerField(default=6, help_text="聯盟中允許的最大玩家數")
    dh_num = models.PositiveIntegerField(default=2)   # 指定打擊數量
    sp_num = models.PositiveIntegerField(default=2)   # 先發投手
    rp_num = models.PositiveIntegerField(default=4)   # 後援投手
    p_num = models.PositiveIntegerField(default=1)    # 自由投手
    bn_num = models.PositiveIntegerField(default=3)   # 板凳球員
    na_num = models.PositiveIntegerField(default=2)   # 禁用球員
    farm_num = models.PositiveIntegerField(default=5) # 農場球員
    il60_num = models.PositiveIntegerField(default=1) # 60天傷兵
    max_rookie_batting_apperances = models.PositiveIntegerField(default=124)
    max_rookie_pitching_innings3 = models.PositiveIntegerField(default=120)

    @property
    def max_rosters(self):
        return 9 + self.dh_num + self.sp_num + self.rp_num + self.p_num + self.bn_num+ self.na_num + self.farm_num + self.il60_num

    @property
    def max_pitcher_num(self):
        return self.sp_num + self.rp_num + self.p_num

    def __str__(self):
        return f"Players = {self.max_players}, Config for {self.league.name} Max Rosters: {self.max_rosters}"
    
class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_leagues')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='LeagueMembership')
    is_public = models.BooleanField(default=True, help_text="是否為公開聯盟，所有人可瀏覽")

    invite_token_mod = models.CharField(max_length=64, blank=True)
    invite_token_player = models.CharField(max_length=64, blank=True)
    invite_token_viewer = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{'公開聯盟' if self.is_public else '未公開聯盟'} {self.name}"

    def generate_invite_tokens(self):
        self.invite_token_mod = secrets.token_urlsafe(24)
        self.invite_token_player = secrets.token_urlsafe(24)
        self.invite_token_viewer = secrets.token_urlsafe(24)
        self.save()

    def get_invite_url(self, role):
        token = getattr(self, f'invite_token_{role}', None)
        if token:
            return f"/leagues/invite/{token}/"
        return "（尚未產生）"

    @property
    def has_draft(self):
        return hasattr(self, 'draft_room')  # ✅ 根據是否有 DraftRoom 判斷
        
class LeagueMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=LEAGUE_ROLE_CHOICES, default='player')

    class Meta:
        unique_together = ('user', 'league')

class FantasyTeam(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')

    class Meta:
        unique_together = ('league', 'name')  # 同一聯盟中隊名不能重複

    def __str__(self):
        return f"{self.name} in {self.league.name}"

class FantasyPlayer(models.Model):
    team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name='players')
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='fantasy_players')
    cpbl_player = models.ForeignKey(CPBLPlayer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'cpbl_player')
        constraints = [
            models.UniqueConstraint(
                fields=['league', 'cpbl_player'],
                name='unique_cpbl_player_per_league'
            )
        ]

    def clean(self):
        # 雙保險：檢查該聯盟中是否已有這位球員
        if FantasyPlayer.objects.filter(
            league=self.league,
            cpbl_player=self.cpbl_player
        ).exclude(pk=self.pk).exists():
            raise ValidationError(f"{self.cpbl_player.name} 已經被選入此聯盟中的其他隊伍。")

    def save(self, *args, **kwargs):
        # 自動同步 league（根據 team）
        if not self.league:
            self.league = self.team.league
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cpbl_player.name} - {self.team.name} ({self.league.name})"