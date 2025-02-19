from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report

@receiver(post_save, sender=Report)
def handle_report_save(sender, instance, created, **kwargs):
    pass  # We'll implement this later for report status notifications
