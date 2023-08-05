
from django import template 
register = template.Library()
from django_img_mobile_vv.utils import *
from django.conf import settings

@register.simple_tag(takes_context=True)
def static_img(context,format_string):
    request = context['request']  
    if(get_and_set_user_agent(request).is_mobile):
         return f"{settings.STATIC_URL}{get_large_or_small_static_img(format_string)}"

    return f"{settings.STATIC_URL}{format_string}" 
 