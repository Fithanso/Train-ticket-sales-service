from django.http import Http404
from django.shortcuts import redirect


class InvalidParametersRedirectMixin:
    # where user should be redirected if get parameters are incorrect
    invalid_parameters_redirect = ''

    def redirect_if_invalid(self):
        if self.invalid_parameters_redirect:
            return redirect(self.invalid_parameters_redirect)
        else:
            raise Http404()
