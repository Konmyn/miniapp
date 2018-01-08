from django.db import models


class MiniBase(models.Model):

    enabled = models.BooleanField(default=True, verbose_name='是否已经删除/禁用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="record create time")
    modidy_time = models.DateTimeField(auto_now=True, verbose_name="record latest modify time")
    remark = models.CharField(max_length=64, verbose_name="remark about this record")

    class Meta:
        abstract = True
