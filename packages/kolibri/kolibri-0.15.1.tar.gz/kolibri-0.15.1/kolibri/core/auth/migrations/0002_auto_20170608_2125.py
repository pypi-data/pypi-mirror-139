# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-08 21:25
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("kolibriauth", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="facilitydataset",
            name="learner_can_login_with_no_password",
            field=models.BooleanField(default=False),
        )
    ]
