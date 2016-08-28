from django.conf.urls import url
from search_img.views import *


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='index'),
]