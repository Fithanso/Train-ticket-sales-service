from django.shortcuts import render


def page_not_found(request, exception=None):
    return render(request, template_name='train_main_app/page404.html', status=404)
