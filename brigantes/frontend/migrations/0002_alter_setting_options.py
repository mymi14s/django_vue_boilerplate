# Generated by Django 5.2.4 on 2025-07-20 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setting',
            options={'verbose_name': 'Site Setting', 'verbose_name_plural': 'Site Settings'},
        ),
    ]
