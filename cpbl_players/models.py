from django.db import models

# Create your models here.

def normalize_name(name):
    return name.replace('　', '').replace(' ', '').strip()

def find_cpbl_player(name, uniform_no):
    norm_name = normalize_name(name)
    try:
        return CPBLPlayer.objects.get(name__icontains=norm_name, jersey_number=uniform_no)
    except CPBLPlayer.DoesNotExist:
        return None
    
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
    
class CPBLPlayerBoxPitcher(models.Model):
    game_sno = models.CharField(max_length=20)
    kind_code = models.CharField(max_length=2, default='A')
    year = models.CharField(max_length=4, default='2024')
    pitcher_name = models.CharField(max_length=100)
    pitcher_uniform_no = models.CharField(max_length=10)
    role = models.CharField(max_length=10)
    result = models.CharField(max_length=10, blank=True)
    bs = models.CharField(max_length=1)
    save = models.IntegerField()
    hold = models.IntegerField()
    inning = models.IntegerField()
    inning_div3 = models.IntegerField()
    pa = models.IntegerField()
    pitch_count = models.IntegerField()
    strike_count = models.IntegerField()
    ball_count = models.IntegerField()
    hits = models.IntegerField()
    hr = models.IntegerField()
    sacrifice_hit = models.IntegerField()
    sacrifice_fly = models.IntegerField()
    bb = models.IntegerField()
    ibb = models.IntegerField()
    hbp = models.IntegerField()
    so = models.IntegerField()
    wp = models.IntegerField()
    bk = models.IntegerField()
    runs = models.IntegerField()
    earned_runs = models.IntegerField()
    max_speed = models.IntegerField()
    mvp = models.CharField(max_length=1)
    error = models.IntegerField()
    date = models.DateField()
    player = models.ForeignKey(CPBLPlayer, null=True, blank=True, on_delete=models.SET_NULL, related_name='pitcher_stats')
    def __str__(self):
        return f"{self.date} - {self.pitcher_name}"
    def save(self, *args, **kwargs):
        if not self.player:
            self.player = find_cpbl_player(self.pitcher_name, self.pitcher_uniform_no)
        super().save(*args, **kwargs)

class CPBLPlayerBoxBatter(models.Model):
    game_sno = models.CharField(max_length=20)
    kind_code = models.CharField(max_length=2, default='A')
    year = models.CharField(max_length=4, default='2024')
    hitter_name = models.CharField(max_length=100)
    hitter_uniform_no = models.CharField(max_length=10)
    pa = models.IntegerField()
    ab = models.IntegerField()
    mvp = models.CharField(max_length=1)
    runs = models.IntegerField()
    hits = models.IntegerField()
    onebase_hits = models.IntegerField()
    twobase_hits = models.IntegerField()
    threebase_hits = models.IntegerField()
    hr = models.IntegerField()
    gs = models.IntegerField()
    total_bases = models.IntegerField()
    dp = models.IntegerField()
    tp = models.IntegerField()
    sacrifice_hit = models.IntegerField()
    sacrifice_fly = models.IntegerField()
    bb = models.IntegerField()
    ibb = models.IntegerField()
    hbp = models.IntegerField()
    so = models.IntegerField()
    sb = models.IntegerField()
    cs = models.IntegerField()
    as_runner_lobs = models.IntegerField()
    as_hitter_lobs = models.IntegerField()
    error = models.IntegerField()
    date = models.DateField()
    player = models.ForeignKey(CPBLPlayer, null=True, blank=True, on_delete=models.SET_NULL, related_name='batter_stats')
    def __str__(self):
        return f"{self.date} - {self.hitter_name}"
    def save(self, *args, **kwargs):
        if not self.player:
            self.player = find_cpbl_player(self.hitter_name, self.hitter_uniform_no)
        super().save(*args, **kwargs)