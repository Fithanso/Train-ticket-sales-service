
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

from .settings import local_fithanso as settings
from .error_handlers import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('train_main_app.urls')),
    path('api/', include('site_api.urls')),
    path('tickets/', include('tickets.urls')),
    path('search/', include('search.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

handler404 = page_not_found
handler500 = page_not_found




