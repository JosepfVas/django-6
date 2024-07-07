from django.db import models

from client.models import Client


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject, self.body

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    )
    first_send_time = models.DateTimeField()
    periodicity = models.CharField(max_length=50,
                                   choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failed', 'Failed')])
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attempt {self.id} - {self.status}"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
