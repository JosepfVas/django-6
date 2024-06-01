from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    comment = models.TextField(**NULLABLE)

    def __str__(self):
        return self.full_name, self.email, self.comment

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
