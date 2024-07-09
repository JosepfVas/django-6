import logging
import pytz
from messenger.models import Mailing, Attempt
from datetime import datetime
from config import settings
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from smtplib import SMTPException
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger('messenger')
  

def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(first_send_time__lte=current_datetime).filter(
        status__in=[Mailing.STATUS_CHOICES]
    )

    for mailing in mailings:
        for client in mailing.clients.all():
            try:
                response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status='success',
                    response=f'Server response: {response}',
                )
                mailing.status = 'success'
                mailing.save()
                print(logger.info(f"Attempt to send mailing {mailing.id} to {client.email} successful"))
            except SMTPException as e:
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status='failed',
                    response=str(e),
                )
                mailing.status = 'failed'
                mailing.save()
                print(logger.error(f"Attempt to send mailing {mailing.id} to {client.email} failed: {e}"))


# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     scheduler.add_job(send_mailing, trigger='cron', minute='*/10')
#     scheduler.start()
