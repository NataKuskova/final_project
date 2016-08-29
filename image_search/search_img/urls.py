from django.conf.urls import url
from search_img.views import *


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='index'),
    url(r'^result/$', ResultView.as_view(), name='result'),
    url(r'^result/(?P<page>\d+)/$', ResultView.as_view(), name='result'),
]