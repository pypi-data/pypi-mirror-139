# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-14 19:33
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0009_merge_20200608_1716"),
    ]

    operations = [
        migrations.CreateModel(
            name="SQLiteLock",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
