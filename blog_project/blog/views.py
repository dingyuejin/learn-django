# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
import logging
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from blog.models import *
from blog.forms import *
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password

# Create your views here.

logger=logging.getLogger("blog_app.views")

def global_setting(request):

    #分类信息
    category_list=Category.objects.all()
    #文章归档数据
    archive_list=Article.objects.distinct_date()
    #标签云
    tag_list=Tag.objects.all()

    # 文章排行榜榜数据
    return {'SITE_NAME':settings.SITE_NAME,
            'SITE_DESC':settings.SITE_DESC,
            'category_list':category_list,
            'tag_list':tag_list,
            'archive_list':archive_list
            }

def index(request):
    try:
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)

    except Exception,e:
        logger.error(e)
    return render(request,'index.html',locals())

# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

def archive(request):
    try:
        year=request.GET.get('year',None)
        month=request.GET.get('month',None)
        article_list=Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list=getPage(request,article_list)
    except Exception,e:
        logger.error(e)
    return render(request,'archive.html',locals())

def tag(request):
    try:
        tag=request.GET.get('tag',None)
        tag=Tag.objects.get(name=tag)
        article_list=tag.article_set.all()
        article_list = getPage(request, article_list)
    except Exception,e:
        logger.error(e)
    return render(request, 'tag.html', locals())


def do_login(request):
    try:
        if request.method=='POST':
            login_form=LoginForm(request.POST)
            if login_form.is_valid():
                username=login_form.cleaned_data["username"]
                password=login_form.cleaned_data["password"]
                user=authenticate(username=username,password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                    return render(request.POST.get('source_url'))
                else:
                    return render(request,'failure.html',{'reason':'登录验证失败'})
            else:
                return render(request,'failure.html',{'reason':login_form.errors})
        else:
            login_form=LoginForm()
    except Exception,e:
        logger.error(e)
    return render(request,'login.html',locals())

# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'article.html', locals())


def do_register(request):
    try:
        if request.method=='POST':
            reg_form=RegForm(request.POST)
            if reg_form.is_valid():
                username=reg_form.clean_data['username']
                email = reg_form.cleaned_data["email"],
                url = reg_form.cleaned_data["url"],
                password = make_password(login_form.cleaned_data["password"])
                user=User.objects.create(
                    user=username,
                    email=email,
                    url=url,
                    password=password
                )
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request,'failure.html',{'reason':reg_form.errors})
        else:
            reg_form=RegForm()
    except Exception,e:
        logger.error(e)
    return render(request,'register.html',locals())

def logout(request):
    try:
        logout(request)
    except Exception,e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])













