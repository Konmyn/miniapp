import uuid
import time

from django.db import models

from base.models import MiniBase
from mall.models import Mall


class MiniApp(MiniBase):
    """
    小程序基本信息
    """
    belongs_to = models.IntegerField(null=False, verbose_name='该小程序归属于哪个商场?')
    appid = models.CharField(max_length=64, db_index=True, null=False, verbose_name='小程序appid')
    secret = models.CharField(max_length=512, default='', verbose_name='小程序secret')
    title = models.CharField(max_length=32, default='', verbose_name='小程序名称')


class MiniAppUser(MiniBase):
    """
    访问小程序的用户
    """
    source = models.ForeignKey(MiniApp, db_index=True, null=False, verbose_name='来源app')
    openid = models.CharField(max_length=64, db_index=True, null=False, verbose_name='用户的openid')
    unionid = models.CharField(max_length=128, default='', verbose_name='用户的unionid')

    class Meta:
        unique_together = (('source', 'openid'),)

    def get_token(self):
        return MiniToken.get_token(self)


class MiniToken(MiniBase):
    """
    小程序的后台api访问token（非腾讯官方相关）
    """
    user = models.ForeignKey(MiniAppUser, db_index=True, null=False, verbose_name='user that this token belongs to')
    token = models.CharField(max_length=64, unique=True, db_index=True, null=False, verbose_name='the token used in api')
    interval = models.IntegerField(default=36000, verbose_name="how long this token will live from generated")
    expire_in = models.IntegerField(default=0, verbose_name="the UTC time this token will expire")
    expired = models.BooleanField(default=False, verbose_name="is this token expired?")

    @classmethod
    def create_token(cls, user, token=None, interval=None):
        if token is None:
            token = uuid.uuid1().hex
        if interval is None:
            interval = 36000
        now = int(time.time())
        expire_in = now + interval
        try:
            cls.objects.create(user=user, token=token, interval=interval, expire_in=expire_in)
        except Exception as e:
            return False
        return token

    @classmethod
    def get_token(cls, user):
        target = None
        now = int(time.time())
        for i in cls.objects.filter(user=user, expired=False):
            if i.expire_in < now:
                i.expired = True
                i.save()
                continue
            if target and target.expire_in < i.expire_in:
                target.expired = True
                target.save()
                target = i
                continue
            target = i
        if target:
            return target.token
        else:
            return cls.create_token(user)

    # 更新token状态，检查token是否过期
    def update_status(self):
        now = int(time.time())
        if self.expire_in < now and self.expired is False:
            self.expired = True
            self.save()
        return self.expired

    def get_mall(self):
        mall_id = self.user.source.belongs_to
        mall = Mall.objects.get(pk=mall_id)
        return mall
