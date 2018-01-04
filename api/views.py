import json
import requests

from django.http import JsonResponse

from base.views import JsonView, HttpBasicView
from mapp.models import MiniApp, MiniAppUser


class TokenView(HttpBasicView):

    def get(self, request, **kwargs):
        result = {
            'code': -1,
            'message': '未知错误',
            'data': None
        }

        code = request.GET.get('code', '')
        appid = request.GET.get('appid', '')
        try:
            mapp = MiniApp.objects.get(appid=appid)
        except MiniApp.DoesNotExist:
            result['message'] = '后台没有配置对应小程序'
            return JsonResponse(result)

        SKEY_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
        url = SKEY_URL.format(appid=appid, secret=mapp.secret, code=code)
        try:
            resp = requests.get(url)
            resp_json = resp.json()
        except Exception as e:
            result['message'] = '访问微信服务器出错'
            return JsonResponse(result)
        if resp_json.get('errcode'):
            result['message'] = resp_json.get('errmsg')
            return JsonResponse(result)
        openid = resp_json.get('openid', '')
        session_key = resp_json.get('session_key', '')
        unionid = resp_json.get('unionid', '')

        muser = MiniAppUser.objects.get_or_create(source=mapp, openid=openid, defaults={'unionid': unionid})
        token = muser.get_token()
        result['code'] = 0
        result['message'] = '请求成功'
        result['data'] = {
            'openid': openid,
            'session_key': session_key,
            'unionid': unionid,
            'token': token
        }
        return JsonResponse(result)


class StoreListView(JsonView):

    def get(self, request, **kwargs):
        result = {
            'code': 0,
            'message': '请求成功',
            'data': [
                {
                    'id': 1,
                    'order': 1,
                    'title': '金拱门',
                    'image': '/media/store/logo/b (1).jpg'
                },
                {
                    'id': 2,
                    'order': 2,
                    'title': '全家桶',
                    'image': '/media/store/logo/b (2).jpg'
                }
            ]
        }
        return JsonResponse(result)


class StoreView(JsonView):

    def get(self, request, store_id=None, **kwargs):
        result = {
            'code': 0,
            'message': '请求成功',
            'data': {
                'id': 1,
                'title': '金拱门',
                'images': [
                    '/media/store/logo/b (4).jpg',
                    '/media/store/brand/b (1).jpg',
                    '/media/store/brand/b (5).jpg',
                    '/media/store/brand/b (6).jpg',
                ],
                'desc': [
                    '这是第一段描述',
                    '这是第二段描述',
                    '这是第三段描述',
                ]
            },
        }
        return JsonResponse(result)
