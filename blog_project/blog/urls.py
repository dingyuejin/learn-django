# coding=utf-8
from django.conf.urls import url
from blog.views import *
urlpatterns=[
    url('^$',index,name='index'),
    url(r'^article/$', article, name='article'),
    url(r'^tag/$',tag,name='tag'),
    url(r'^archive/$',archive,name='archive')
]