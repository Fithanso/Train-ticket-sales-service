from django import template

from ..models import SiteSetting

register = template.Library()


@register.simple_tag()
def currency_sign():
    return SiteSetting.get_setting('currency_sign')


@register.simple_tag()
def currency_name():
    return SiteSetting.get_setting('currency_name')
