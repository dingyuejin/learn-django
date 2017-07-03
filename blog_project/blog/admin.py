from django.contrib import admin
from models import *
# Register your models here.

# class ArticleAdmin(admin.ModelAdmin):
#     exclude = ('title','desc')

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)