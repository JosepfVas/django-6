# Generated by Django 4.2.2 on 2024-06-08 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='last_send_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
