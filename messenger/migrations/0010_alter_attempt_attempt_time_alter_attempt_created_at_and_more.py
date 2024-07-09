# Generated by Django 4.2.2 on 2024-07-07 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_client_comment_alter_client_email_and_more'),
        ('messenger', '0009_mailing_owner_message_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='attempt_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='попытка рассылки'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='response',
            field=models.TextField(blank=True, null=True, verbose_name='ответ сервера'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='status',
            field=models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], max_length=50, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='client',
            field=models.ManyToManyField(to='client.client', verbose_name='клиент'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='first_send_time',
            field=models.DateTimeField(verbose_name='время первой отправки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='last_send_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время конечной отправки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messenger.message', verbose_name='сообщение'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='next_send_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время следующей отправки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='periodicity',
            field=models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=50, verbose_name='периодичность'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('started', 'Started'), ('completed', 'Completed'), ('failed', 'Failed')], default='created', max_length=50, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='тело сообщения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='оглавление сообщения'),
        ),
    ]