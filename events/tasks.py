from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_event_notification(subject: str, message: str, to_email: str):
    """
    Simple Celery task to demonstrate async execution.
    Uses console email backend for local development.
    """
    send_mail(subject, message, "no-reply@example.com", [to_email], fail_silently=True)

