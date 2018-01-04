import base64
from functools import wraps

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator


def basic_auth_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META.keys():
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = base64.b64decode(auth.strip()).decode()
                username, password = auth.split(':', 1)
                if username == 'wxmall' and password == 'wxmall':
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden('<h1>Forbidden</h1>')
        res = HttpResponse()
        res.status_code = 401
        res['WWW-Authenticate'] = 'Basic'
        return res
    return wrapper


class HttpBasicView(View):
    @csrf_exempt
    @method_decorator(basic_auth_required)
    def dispatch(self, *args, **kwargs):
        return super(HttpBasicView, self).dispatch(*args, **kwargs)


class JsonView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(JsonView, self).dispatch(*args, **kwargs)
