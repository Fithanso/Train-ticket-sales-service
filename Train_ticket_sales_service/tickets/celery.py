import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Train_ticket_sales_service.settings.local_fithanso")
app = Celery("tickets")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

#  python -m celery -A tickets worker -l info -P solo
