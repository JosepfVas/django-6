from django.db import models
from client.models import Client, NULLABLE
from users.models import User


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='оглавление сообщения')
    body = models.TextField(verbose_name='тело сообщения')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    CREATED = 'created'
    COMPLETED = 'completed'
    STARTED = 'started'
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    first_send_time = models.DateTimeField(verbose_name='время первой отправки')
    last_send_time = models.DateTimeField(**NULLABLE, verbose_name='время конечной отправки')
    next_send_time = models.DateTimeField(**NULLABLE, verbose_name='время следующей отправки')
    periodicity = models.CharField(max_length=50,
                                   choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
                                   default='daily', verbose_name='периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created', verbose_name='статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    client = models.ManyToManyField(Client, verbose_name='клиент')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return (f'{self.status} {self.message} {self.first_send_time} {self.last_send_time} {self.periodicity} '
                f'{self.client}')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [("can_change_status", "Может менять статус")]


class Attempt(models.Model):
    SUCCESS = 'successful'
    FAIL = 'failed'
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, **NULLABLE)
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='попытка рассылки')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='статус')
    response = models.TextField(blank=True, null=True, verbose_name='ответ сервера')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')

    def __str__(self):
        return f'{self.status} {self.created_at} {self.response} {self.attempt_time} {self.client}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
