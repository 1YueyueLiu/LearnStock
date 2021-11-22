# Generated by Django 2.1.5 on 2021-11-22 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12)),
                ('content', models.CharField(max_length=128)),
                ('posttime', models.DateTimeField(default=datetime.datetime(2021, 11, 22, 15, 27, 54, 541296))),
                ('category', models.SlugField()),
            ],
        ),
    ]