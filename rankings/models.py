from django.db import models
from django.contrib.auth import get_user_model
from cpbl_players.models import CPBLPlayer

class RankingRecord(models.Model):
    id = models.AutoField(primary_key=True)

    RANK_TYPE_CHOICES = [
        ('batter', 'Batter'),
        ('pitcher', 'Pitcher'),
    ]

    rank_type = models.CharField(max_length=10, choices=RANK_TYPE_CHOICES)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} {self.get_rank_type_display()} Ranking ({self.start_date} ~ {self.end_date})"
    
class RankingPitcherDetail(models.Model):
    ranking_record = models.ForeignKey(RankingRecord, on_delete=models.CASCADE, related_name='pitcher_details')
    player = models.ForeignKey(CPBLPlayer, on_delete=models.CASCADE)
    ranking= models.IntegerField(default=0)
    mvp = models.IntegerField(default=0)  # 21
    ip = models.FloatField(default=0)  # 11
    wqs = models.IntegerField(default=0)  # 12
    h = models.IntegerField(default=0)  # 13
    sv = models.IntegerField(default=0)  # 14
    so = models.IntegerField(default=0)  # 15
    fip = models.FloatField(default=0)  # 16
    era = models.FloatField(default=0)  # 17
    whip = models.FloatField(default=0)  # 18
    runs = models.IntegerField(default=0)  # 19
    free_bases = models.IntegerField(default=0)  # 20（WP+BK+E）

    def __str__(self):
        return f"{self.ranking} - {self.player}"
class RankingBatterDetail(models.Model):
    ranking_record = models.ForeignKey(RankingRecord, on_delete=models.CASCADE, related_name='batter_details')
    player = models.ForeignKey(CPBLPlayer, on_delete=models.CASCADE)
    ranking= models.IntegerField(default=0)
    rrbi = models.IntegerField(default=0)  # 1 R+RBI
    hr = models.IntegerField(default=0)  # 2
    tb = models.IntegerField(default=0)  # 3
    bbbbb = models.IntegerField(default=0)  # 4 BB+IBB+HBP
    avg = models.FloatField(default=0)  # 5
    obp = models.FloatField(default=0)  # 6
    isop = models.FloatField(default=0)  # 7 SLG-AVG
    sb = models.IntegerField(default=0)  # 8
    shf = models.IntegerField(default=0)  # 9 SH+SF
    dopes = models.IntegerField(default=0)  # 10 DP+E+SO
    mvp = models.IntegerField(default=0)  # 21

    def __str__(self):
        return f"{self.ranking} - {self.player}"