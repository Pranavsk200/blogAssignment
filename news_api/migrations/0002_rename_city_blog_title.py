# Generated by Django 3.2.8 on 2022-11-27 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='city',
            new_name='title',
        ),
    ]
