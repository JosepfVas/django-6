from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержимое статьи")
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата публикации', **NULLABLE)

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title
