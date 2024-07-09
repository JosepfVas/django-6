from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='почта')
    full_name = models.CharField(max_length=150, verbose_name='полное имя')
    comment = models.TextField(**NULLABLE, verbose_name='о клиенте')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
