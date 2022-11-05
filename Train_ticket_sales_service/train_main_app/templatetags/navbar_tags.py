from django import template
from django.shortcuts import reverse

from ..models import Country

register = template.Library()


@register.simple_tag()
def get_available_countries():
    return Country.objects.filter(available=1)


@register.simple_tag()
def get_link_to_index():
    return reverse('index')

