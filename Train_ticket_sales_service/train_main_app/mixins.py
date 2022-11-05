from django.http import Http404
from django.shortcuts import redirect


class InvalidParametersRedirectMixin:
    # where user should be redirected if get parameters are incorrect
    redirect_to_if_invalid = ''

    def redirect_if_invalid(self):
        if self.redirect_to_if_invalid:
            return redirect(self.redirect_to_if_invalid)
        else:
            raise Http404()
