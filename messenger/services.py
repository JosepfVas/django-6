import smtplib
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from messenger.models import Mailing, Attempt


def send_letters():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    print(f'Локальное время: {current_datetime}, зона: {zone}')

    mailings = Mailing.objects.filter(first_send_time__lte=current_datetime,
                                      status__in=[Mailing.STARTED, Mailing.CREATED])
    print(f'Количество рассылок для отправки: {mailings.count()}')
    for mailing in mailings:
        print(f'Рассылка ID: {mailing.id}, first_send_time: {mailing.first_send_time}')
        mailing.status = Mailing.STARTED
        mailing.save()
        clients = mailing.client.all()

        try:
            recipient_list = [client.email for client in clients]
            if not recipient_list:
                print(f'Рассылка ID: {mailing.id} не имеет получателей.')
                continue

            server_response = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            if server_response == 0:
                print(f'Рассылка ID: {mailing.id} не была отправлена. Ответ сервера: {server_response}')
                Attempt.objects.create(attempt_time=mailing.first_send_time, status='failed',
                                       response=str(server_response),
                                       mailing=mailing)
            else:
                print(f'Рассылка ID: {mailing.id} успешно отправлена. Ответ сервера: {server_response}')
                Attempt.objects.create(attempt_time=mailing.first_send_time, status='success',
                                       response=server_response, mailing=mailing)
        except smtplib.SMTPException as e:
            print(f'Ошибка при отправке рассылки ID: {mailing.id}. Ошибка: {e}')
            Attempt.objects.create(attempt_time=mailing.first_send_time, status=Attempt.FAIL, response=str(e),
                                   mailing=mailing)

        if mailing.periodicity == 'daily':
            mailing.last_send_time += timedelta(days=1)
        elif mailing.periodicity == 'weekly':
            mailing.last_send_time += timedelta(weeks=1)
        elif mailing.periodicity == 'monthly':
            mailing.last_send_time += timedelta(days=30)

        mailing.save()
        print(f'Обновленное last_send_time для рассылки ID: {mailing.id}: {mailing.last_send_time}')


def start_scheduler():
    print('Starting scheduler...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_letters, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()

    print('Scheduler started')
