# Generated by Django 3.2.8 on 2022-11-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=60)),
                ('content', models.TextField()),
                ('createdAt', models.DateTimeField()),
            ],
        ),
    ]
