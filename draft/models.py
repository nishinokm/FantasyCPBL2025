from django.db import models
from fb_leagues.models import League, FantasyTeam
from cpbl_players.models import CPBLPlayer

class DraftRoom(models.Model):
    DRAFT_TYPE_CHOICES = [
        ('snake', 'Snake'),
        ('normal', 'Normal'),
    ]

    league = models.OneToOneField(League, on_delete=models.CASCADE, related_name='draft_room')
    draft_type = models.CharField(max_length=10, choices=DRAFT_TYPE_CHOICES, default='snake')
    current_round = models.PositiveIntegerField(default=1)
    current_pick = models.PositiveIntegerField(default=1)
    max_round = models.PositiveIntegerField(default=20)
    min_giveup_round = models.PositiveIntegerField(default=16)
    top_n_round_for_draw = models.PositiveIntegerField(default=1)
    is_complete = models.BooleanField(default=False)
    draft_timeouts = models.PositiveIntegerField(default=60)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DraftRoom for {self.league.name}"

class DraftUnit(models.Model):
    draft = models.ForeignKey(DraftRoom, on_delete=models.CASCADE, related_name='units')
    round = models.PositiveIntegerField()
    pick = models.PositiveIntegerField()
    ori_owner = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name='original_picks')
    new_owner = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name='actual_picks')
    pre_draft = models.BooleanField(default=False)
    player = models.ForeignKey(CPBLPlayer, on_delete=models.SET_NULL, null=True, blank=True)
    pick_at_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('draft', 'round', 'pick')
        ordering = ['round', 'pick']

    def __str__(self):
        return f"Round {self.round}, Pick {self.pick} by {self.new_owner.name}"
