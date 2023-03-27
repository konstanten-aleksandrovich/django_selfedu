from django import template
from women.models import *

register=template.Library()

@register.simple_tag(name='getcats')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None,cat_selected=0):
    if sort:
        cat=Category.objects.all()
    else:
        cat=Category.objects.order_by(sort)
    return {'cats':cat,"cat_selected":cat_selected}