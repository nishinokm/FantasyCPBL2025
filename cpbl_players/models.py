from django.db import models

# Create your models here.

class CPBLPlayer(models.Model):
    player_id = models.PositiveIntegerField(unique=True)  # 從 10001 開始，需在資料庫層面設定初始值
    team_id = models.PositiveIntegerField()
    jersey_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    isForeign = models.BooleanField(default=False)
    isRookie = models.BooleanField(default=True)
    wasAbroad = models.BooleanField(default=False)
    pitching_hand = models.CharField(max_length=1, choices=[('L', 'Left'), ('R', 'Right'), ('S', 'Switch')])
    batting_hand = models.CharField(max_length=1, choices=[('L', 'Left'), ('R', 'Right'), ('S', 'Switch')])
    main_pos = models.CharField(max_length=30)
    batting_games = models.PositiveIntegerField(default=0)
    batting_appearances = models.PositiveIntegerField(default=0)
    pitching_games = models.PositiveIntegerField(default=0)
    pitching_innings3 = models.PositiveIntegerField(default=0)
    is_injured = models.BooleanField(default=False)
    sp_games = models.PositiveIntegerField(default=0)
    rp_games = models.PositiveIntegerField(default=0)
    c_games = models.PositiveIntegerField(default=0)
    _1b_games = models.PositiveIntegerField(default=0)
    _2b_games = models.PositiveIntegerField(default=0)
    _3b_games = models.PositiveIntegerField(default=0)
    ss_games = models.PositiveIntegerField(default=0)
    of_games = models.PositiveIntegerField(default=0)
    lf_games = models.PositiveIntegerField(default=0)
    cf_games = models.PositiveIntegerField(default=0)
    rf_games = models.PositiveIntegerField(default=0)
    mvp_counts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class CPBLPlayerStats(models.Model):
    player = models.OneToOneField(CPBLPlayer, on_delete=models.CASCADE, related_name='stats')
    year = models.PositiveIntegerField()
    games_played = models.PositiveIntegerField()
    hits = models.PositiveIntegerField()
    home_runs = models.PositiveIntegerField()
    rbi = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.player.name} ({self.year})"