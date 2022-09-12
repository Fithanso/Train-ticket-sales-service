# had to remove it from business_logic due to different import errors which I didn't understand how to solve
from django.shortcuts import redirect
from django.utils.text import slugify

import pycountry
from ip2geotools.databases.noncommercial import DbIpCity

from .business_logic.detailed_model_info_providers import SiteSettingInfoGetter
from .models import SiteSetting
from .constants import COUNTRY_NOT_FOUND_VALUE


class RedirectToUsersCountry:

    def __init__(self, request):
        self.request = request
        self._user_ip = ''

    def get(self):
        self._user_ip = self._get_user_ip()
        country_name = self._get_users_country_or_default()

        return redirect('voyages_filter', country_slug=country_name)

    def _get_user_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = self.request.META.get('REMOTE_ADDR')

        return user_ip

    def _get_users_country_or_default(self) -> str:
        default_country = SiteSetting.objects.get(name='default_country')
        region_code = DbIpCity.get(self._user_ip, api_key='free').country

        if region_code == COUNTRY_NOT_FOUND_VALUE:
            return default_country

        country_name = slugify(pycountry.countries.get(alpha_2=region_code).name)

        return country_name if SiteSettingInfoGetter.country_available(country_name) else default_country
