# -*- coding: utf-8 -*-

from . import views
from django.conf.urls import url

app_name = 'crawl'

urlpatterns = [
    url(r'^$', views.crawl_site.index, name='index'),
]
