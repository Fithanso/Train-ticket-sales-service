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
    path('', include('train_main_app.urls')),
    path('api/', include('train_main_app.api_urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

handler404 = page_not_found
handler500 = page_not_found




