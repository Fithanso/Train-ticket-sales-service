from django import template
from django.shortcuts import reverse

from ..models import SiteSetting

register = template.Library()


@register.simple_tag()
def get_available_countries():
    return SiteSetting.get_available_countries()


@register.simple_tag()
def get_link_to_index():
    return reverse('index')

