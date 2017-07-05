# coding=utf-8
from django.conf.urls import url
from blog.views import *
urlpatterns=[
    url('^$',index,name='index'),
    url(r'^article/$', article, name='article'),
    url(r'^tag/$',tag,name='tag'),
    url(r'^archive/$',archive,name='archive'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^comment_post/$',comment_post,name='comment_post'),
    url(r'^login/$',do_login,name='login'),
    url(r'^reg/$',do_register,name='reg')
]