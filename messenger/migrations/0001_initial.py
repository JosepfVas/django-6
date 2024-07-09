# Generated by Django 4.2.2 on 2024-06-08 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_send_time', models.DateTimeField()),
                ('periodicity', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=50)),
                ('status', models.CharField(choices=[('created', 'Created'), ('started', 'Started'), ('completed', 'Completed')], default='created', max_length=50)),
                ('clients', models.ManyToManyField(to='client.client')),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='messenger.message')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], max_length=50)),
                ('response', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='messenger.mailing')),
            ],
            options={
                'verbose_name': 'Попытка',
                'verbose_name_plural': 'Попытки',
            },
        ),
    ]
