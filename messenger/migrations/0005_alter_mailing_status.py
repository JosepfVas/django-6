# Generated by Django 4.2.2 on 2024-06-09 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_alter_mailing_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('started', 'Started'), ('completed', 'Completed'), ('failed', 'Failed')], default='created', max_length=50),
        ),
    ]
