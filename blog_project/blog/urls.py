# coding=utf-8
from django.conf.urls import url
from blog.views import *
urlpatterns=[
    url('^$',index,name='index'),
    url(r'^article/$', article, name='article'),
]