# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-22 20:44
from __future__ import unicode_literals

from django.db import migrations

import kolibri.core.auth.models


class Migration(migrations.Migration):

    dependencies = [("kolibriauth", "0007_auto_20171226_1125")]

    operations = [
        migrations.AlterModelManagers(
            name="facilityuser",
            managers=[("objects", kolibri.core.auth.models.FacilityUserModelManager())],
        )
    ]
