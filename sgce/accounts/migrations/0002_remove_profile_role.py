# Generated by Django 2.0.7 on 2018-07-09 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
    ]