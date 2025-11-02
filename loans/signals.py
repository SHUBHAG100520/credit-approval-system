import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .tasks import ingest_from_excel

@receiver(post_migrate)
def trigger_initial_ingest(sender, **kwargs):
    if os.path.exists("data/customer_data.xlsx") and os.path.exists("data/loan_data.xlsx"):
        ingest_from_excel.delay("data/customer_data.xlsx", "data/loan_data.xlsx")
