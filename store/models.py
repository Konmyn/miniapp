from django.db import models

from base.models import MiniBase


class Store(MiniBase):
    mall = models.CharField(max_length=64, verbose_name='所属商场id')
    floor = models.CharField(max_length=64, verbose_name='所属楼层')
    title = models.CharField(max_length=128, db_index=True, null=False, verbose_name="商铺名称")
    brief = models.CharField(max_length=256, default='', verbose_name='商铺简介')
    desc = models.TextField(default='', verbose_name="详细描述")
    # addr = models.CharField(max_length=50, null=True, verbose_name="详细地址")
    # logo = models.FileField(upload_to='store/logo/', verbose_name='品牌图标', null=True)
    # brand = models.FileField(upload_to='store/brand/', verbose_name='品牌图片', null=True)
    # mobile = models.CharField(max_length=50, null=True, verbose_name="联系电话")
    # category = models.CharField(max_length=100, null=True, verbose_name="分类")

