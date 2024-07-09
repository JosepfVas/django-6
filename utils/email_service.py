from django.core.mail import send_mail
import logging
import os

logger = logging.getLogger(__name__)


def send_email(recipient_email, subject, body):
    try:
        send_mail(
            subject,
            body,
            os.getenv('EMAIL_HOST_USER'),
            [recipient_email],
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки почты на email: {recipient_email}: {e}")
        raise e
