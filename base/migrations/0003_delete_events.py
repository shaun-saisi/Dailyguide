# Generated by Django 4.2.7 on 2023-11-19 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_events'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Events',
        ),
    ]