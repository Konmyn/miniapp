from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import MiniBase


class User(AbstractUser, MiniBase):
    """
    后台用户
    """
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name="姓名")
    uuid = models.CharField(max_length=64, verbose_name="用户全局唯一标识", db_index=True, null=False, unique=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
