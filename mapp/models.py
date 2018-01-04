from django.db import models

from base.models import MiniBase


class MiniApp(MiniBase):
    """
    小程序基本信息
    """
    appid = models.CharField(max_length=64, db_index=True, null=False, verbose_name='小程序appid')
    secret = models.CharField(max_length=512, default='', verbose_name='小程序secret')
    title = models.CharField(max_length=32, default='', verbose_name='小程序名称')
    enabled = models.BooleanField(default=True, verbose_name='小程序是否开启')


class MiniAppUser(MiniBase):
    """
    访问小程序的用户
    """
    source = models.ForeignKey(MiniApp, db_index=True, null=False, verbose_name='来源app')
    openid = models.CharField(max_length=64, db_index=True, null=False, verbose_name='用户的openid')
    unionid = models.CharField(max_length=128, default='', verbose_name='用户的unionid')

    class Meta:
        unique_together = (('source', 'openid'),)
