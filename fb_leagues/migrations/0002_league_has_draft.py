# Generated by Django 4.2.8 on 2025-03-21 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='has_draft',
            field=models.BooleanField(default=False, help_text='是否已經進行過選秀'),
        ),
    ]
