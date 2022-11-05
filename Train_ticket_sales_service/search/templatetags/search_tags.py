from django import template
from train_main_app.models import SiteSetting

register = template.Library()


@register.inclusion_tag('search/purchase_button.html')
def create_purchase_button(voyage, for_page: str):

    state = 'buy_available'
    buyable = SiteSetting.get_setting('old_tickets_buyable').value

    if voyage.expired:
        if buyable == 'True':
            state = 'buy_warning'
        else:
            state = 'buy_unavailable'

    return {'voyage': voyage, 'state': state, 'for_page': for_page}
