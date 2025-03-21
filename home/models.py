# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # 與內建 User 模型關聯
    nickname = models.TextField()                 # 暱稱
    role = models.TextField()                     # 角色 (代表 user 的 group)
    join_leagues = models.TextField()             # 加入的聯盟

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

#__MODELS__

#__MODELS__END
