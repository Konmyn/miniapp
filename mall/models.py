from django.db import models

from base.models import MiniBase


class Mall(MiniBase):
    title = models.CharField(max_length=32, null=False, verbose_name='商场名称')
    address = models.CharField(max_length=128, default='', verbose_name='商场地址')

