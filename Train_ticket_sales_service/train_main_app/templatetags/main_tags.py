from django import template

from ..business_logic.detailed_model_info_providers import SiteSettingInfoGetter

register = template.Library()


@register.simple_tag()
def currency_sign():
    return SiteSettingInfoGetter.get_currency_sign()


@register.simple_tag()
def currency_name():
    return SiteSettingInfoGetter.get_currency_name()
