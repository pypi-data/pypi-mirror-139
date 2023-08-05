# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-27 19:59
from __future__ import unicode_literals

import django.db.models.deletion
import morango.models.fields.uuids
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("kolibriauth", "0019_collection_no_mptt"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    morango.models.fields.uuids.UUIDField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "_morango_dirty_bit",
                    models.BooleanField(default=True, editable=False),
                ),
                ("_morango_source_id", models.CharField(editable=False, max_length=96)),
                (
                    "_morango_partition",
                    models.CharField(editable=False, max_length=128),
                ),
                (
                    "content_id",
                    morango.models.fields.uuids.UUIDField(blank=True, null=True),
                ),
                (
                    "channel_id",
                    morango.models.fields.uuids.UUIDField(blank=True, null=True),
                ),
                ("contentnode_id", morango.models.fields.uuids.UUIDField()),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kolibriauth.FacilityDataset",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="bookmark",
            unique_together=set([("user", "contentnode_id")]),
        ),
    ]
