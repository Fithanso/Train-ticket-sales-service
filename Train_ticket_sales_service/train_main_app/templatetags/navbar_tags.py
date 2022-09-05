from django import template
from django.shortcuts import reverse

from ..business_logic.detailed_model_info_providers import SiteSettingInfoGetter

register = template.Library()


@register.simple_tag()
def get_available_countries():
    return SiteSettingInfoGetter.get_available_countries()


@register.simple_tag()
def get_link_to_index():
    return reverse('index')

