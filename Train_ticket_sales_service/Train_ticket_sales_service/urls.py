"""Train_ticket_sales_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

sys.path.append('C:\\Users\\Matvey\\PycharmProjects\\Akhenaton\\Train_ticket_sales_service\\Train_ticket_sales_service')
sys.path.append('C:\\Users\\Matvey\\PycharmProjects\\Akhenaton\\Train_ticket_sales_service\\train_main_app')

import settings
from error_handlers import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('train_main_app.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

handler404 = page_not_found
handler500 = page_not_found




