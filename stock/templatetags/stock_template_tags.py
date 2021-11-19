from django import template
from stock.models import Category

register = template.Library()

@register.inclusion_tag('stock/categories.html')
def get_category_list(current_category=None):
    return{'categories':Category.objects.all(),
          'current_categories':current_category}

