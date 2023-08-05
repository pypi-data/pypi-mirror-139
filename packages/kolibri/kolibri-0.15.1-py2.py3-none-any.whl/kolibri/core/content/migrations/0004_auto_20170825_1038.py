# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-25 17:38
from __future__ import unicode_literals

import django.db.models.deletion
import django.db.models.manager
import morango.models
import mptt.fields
from django.db import migrations
from django.db import models

import kolibri.core.fields


class Migration(migrations.Migration):

    dependencies = [("content", "0003_auto_20170607_1212")]

    operations = [
        migrations.CreateModel(
            name="AssessmentMetaData",
            fields=[
                ("id", morango.models.UUIDField(primary_key=True, serialize=False)),
                ("assessment_item_ids", kolibri.core.fields.JSONField(default=[])),
                ("number_of_assessments", models.IntegerField()),
                ("mastery_model", kolibri.core.fields.JSONField(default={})),
                ("randomize", models.BooleanField(default=False)),
                ("is_manipulable", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="ChannelMetadata",
            fields=[
                ("id", morango.models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                ("description", models.CharField(blank=True, max_length=400)),
                ("author", models.CharField(blank=True, max_length=400)),
                ("version", models.IntegerField(default=0)),
                ("thumbnail", models.TextField(blank=True)),
                ("last_updated", kolibri.core.fields.DateTimeTzField(null=True)),
                ("min_schema_version", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="ContentNode",
            fields=[
                ("id", morango.models.UUIDField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("content_id", morango.models.UUIDField(db_index=True)),
                ("channel_id", morango.models.UUIDField(db_index=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=400, null=True),
                ),
                ("sort_order", models.FloatField(blank=True, null=True)),
                ("license_owner", models.CharField(blank=True, max_length=200)),
                ("author", models.CharField(blank=True, max_length=200)),
                (
                    "kind",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("topic", "Topic"),
                            ("video", "Video"),
                            ("audio", "Audio"),
                            ("exercise", "Exercise"),
                            ("document", "Document"),
                            ("html5", "HTML5 App"),
                        ],
                        max_length=200,
                    ),
                ),
                ("available", models.BooleanField(default=False)),
                ("stemmed_metaphone", models.CharField(blank=True, max_length=1800)),
                ("lft", models.PositiveIntegerField(db_index=True, editable=False)),
                ("rght", models.PositiveIntegerField(db_index=True, editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(db_index=True, editable=False)),
                (
                    "has_prerequisite",
                    models.ManyToManyField(
                        blank=True,
                        related_name="prerequisite_for",
                        to="content.ContentNode",
                    ),
                ),
            ],
            options={"ordering": ("lft",)},
            # Removed because django-mptt 0.8.7 patched up an error in
            # Django 1.9 (fixed since 1.10).
            # Ref: https://code.djangoproject.com/ticket/26643
            # https://github.com/learningequality/kolibri/pull/3180
            # managers=[
            #     ('_default_manager', django.db.models.manager.Manager()),
            # ],
            # Removed with the same reasoning
            # managers=[
            #     ('objects', django.db.models.manager.Manager()),
            # ],
        ),
        migrations.CreateModel(
            name="ContentTag",
            fields=[
                ("id", morango.models.UUIDField(primary_key=True, serialize=False)),
                ("tag_name", models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                ("id", morango.models.UUIDField(primary_key=True, serialize=False)),
                ("available", models.BooleanField(default=False)),
                (
                    "preset",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("high_res_video", "High Resolution"),
                            ("low_res_video", "Low Resolution"),
                            ("vector_video", "Vectorized"),
                            ("video_thumbnail", "Thumbnail"),
                            ("video_subtitle", "Subtitle"),
                            ("audio", "Audio"),
                            ("audio_thumbnail", "Thumbnail"),
                            ("document", "Document"),
                            ("document_thumbnail", "Thumbnail"),
                            ("exercise", "Exercise"),
                            ("exercise_thumbnail", "Thumbnail"),
                            ("exercise_image", "Exercise Image"),
                            ("exercise_graphie", "Exercise Graphie"),
                            ("channel_thumbnail", "Channel Thumbnail"),
                            ("topic_thumbnail", "Thumbnail"),
                            ("html5_zip", "HTML5 Zip"),
                            ("html5_thumbnail", "HTML5 Thumbnail"),
                        ],
                        max_length=150,
                    ),
                ),
                ("supplementary", models.BooleanField(default=False)),
                ("thumbnail", models.BooleanField(default=False)),
                ("priority", models.IntegerField(blank=True, db_index=True, null=True)),
                (
                    "contentnode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="content.ContentNode",
                    ),
                ),
            ],
            options={"ordering": ["priority"]},
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.CharField(max_length=14, primary_key=True, serialize=False),
                ),
                ("lang_code", models.CharField(db_index=True, max_length=3)),
                (
                    "lang_subcode",
                    models.CharField(
                        blank=True, db_index=True, max_length=10, null=True
                    ),
                ),
                ("lang_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "lang_direction",
                    models.CharField(
                        choices=[("ltr", "Left to Right"), ("rtl", "Right to Left")],
                        default="ltr",
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("license_name", models.CharField(max_length=50)),
                (
                    "license_description",
                    models.CharField(blank=True, max_length=400, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LocalFile",
            fields=[
                (
                    "id",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                (
                    "extension",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("mp4", "MP4 Video"),
                            ("vtt", "VTT Subtitle"),
                            ("srt", "SRT Subtitle"),
                            ("mp3", "MP3 Audio"),
                            ("pdf", "PDF Document"),
                            ("jpg", "JPG Image"),
                            ("jpeg", "JPEG Image"),
                            ("png", "PNG Image"),
                            ("gif", "GIF Image"),
                            ("json", "JSON"),
                            ("svg", "SVG Image"),
                            ("perseus", "Perseus Exercise"),
                            ("zip", "HTML5 Zip"),
                        ],
                        max_length=40,
                    ),
                ),
                ("available", models.BooleanField(default=False)),
                ("file_size", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(name="ChannelMetadataCache"),
        migrations.AddField(
            model_name="file",
            name="lang",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="content.Language",
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="local_file",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="content.LocalFile",
            ),
        ),
        migrations.AddField(
            model_name="contentnode",
            name="lang",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="content.Language",
            ),
        ),
        migrations.AddField(
            model_name="contentnode",
            name="license",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="content.License",
            ),
        ),
        migrations.AddField(
            model_name="contentnode",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="content.ContentNode",
            ),
        ),
        migrations.AddField(
            model_name="contentnode",
            name="related",
            field=models.ManyToManyField(
                blank=True,
                related_name="_contentnode_related_+",
                to="content.ContentNode",
            ),
        ),
        migrations.AddField(
            model_name="contentnode",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tagged_content", to="content.ContentTag"
            ),
        ),
        migrations.AddField(
            model_name="channelmetadata",
            name="root",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="content.ContentNode"
            ),
        ),
        migrations.AddField(
            model_name="assessmentmetadata",
            name="contentnode",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assessmentmetadata",
                to="content.ContentNode",
            ),
        ),
    ]
