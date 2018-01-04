from django.conf.urls import url


from api.views import *

urlpatterns = [
    url(r'^v1/token$', TokenView.as_view(), name='token'),
    url(r'^v1/store$', StoreListView.as_view(), name='store.list'),
    url(r'^v1/store/(?P<store_id>\d+)$', StoreView.as_view(), name='store.detail'),
]
