# Generated by Django 2.2.17 on 2020-11-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_event_public_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='has_public_page',
            field=models.BooleanField(default=False, help_text='teste', verbose_name='Tem página pública?'),
        ),
    ]
