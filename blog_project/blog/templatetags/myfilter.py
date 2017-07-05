# -*- coding: utf-8 -*-
from django import template
register=template.Library()
@register.filter
def month_to_upper(value):
    month=value.month
    return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][month-1]