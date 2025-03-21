# Generated by Django 4.2.8 on 2025-03-21 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpbl_players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('league_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('is_public', models.BooleanField(default=True, help_text='是否為公開聯盟，所有人可瀏覽')),
                ('invite_token_mod', models.CharField(blank=True, max_length=64)),
                ('invite_token_player', models.CharField(blank=True, max_length=64)),
                ('invite_token_viewer', models.CharField(blank=True, max_length=64)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_leagues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('mod', 'Moderator'), ('player', 'Player'), ('viewer', 'Viewer')], default='player', max_length=10)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_leagues.league')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'league')},
            },
        ),
        migrations.CreateModel(
            name='LeagueConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_name', models.CharField(default='預設配置', max_length=100)),
                ('max_players', models.PositiveIntegerField(default=6, help_text='聯盟中允許的最大玩家數')),
                ('dh_num', models.PositiveIntegerField(default=2)),
                ('sp_num', models.PositiveIntegerField(default=2)),
                ('rp_num', models.PositiveIntegerField(default=4)),
                ('p_num', models.PositiveIntegerField(default=1)),
                ('bn_num', models.PositiveIntegerField(default=3)),
                ('na_num', models.PositiveIntegerField(default=2)),
                ('farm_num', models.PositiveIntegerField(default=5)),
                ('il60_num', models.PositiveIntegerField(default=1)),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='fb_leagues.league')),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='members',
            field=models.ManyToManyField(through='fb_leagues.LeagueMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FantasyTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='fb_leagues.league')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('league', 'name')},
            },
        ),
        migrations.CreateModel(
            name='FantasyPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpbl_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpbl_players.cpblplayer')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fantasy_players', to='fb_leagues.league')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='fb_leagues.fantasyteam')),
            ],
        ),
        migrations.AddConstraint(
            model_name='fantasyplayer',
            constraint=models.UniqueConstraint(fields=('league', 'cpbl_player'), name='unique_cpbl_player_per_league'),
        ),
        migrations.AlterUniqueTogether(
            name='fantasyplayer',
            unique_together={('team', 'cpbl_player')},
        ),
    ]
