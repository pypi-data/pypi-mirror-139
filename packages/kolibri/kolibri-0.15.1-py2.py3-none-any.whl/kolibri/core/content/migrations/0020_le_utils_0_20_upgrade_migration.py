# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-22 17:32
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("content", "0019_contentnode_slideshow_options")]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="preset",
            field=models.CharField(
                blank=True,
                choices=[
                    ("high_res_video", "High Resolution"),
                    ("low_res_video", "Low Resolution"),
                    ("video_thumbnail", "Thumbnail"),
                    ("video_subtitle", "Subtitle"),
                    ("video_dependency", "Video (dependency)"),
                    ("audio", "Audio"),
                    ("audio_thumbnail", "Thumbnail"),
                    ("document", "Document"),
                    ("epub", "ePub Document"),
                    ("document_thumbnail", "Thumbnail"),
                    ("exercise", "Exercise"),
                    ("exercise_thumbnail", "Thumbnail"),
                    ("exercise_image", "Exercise Image"),
                    ("exercise_graphie", "Exercise Graphie"),
                    ("channel_thumbnail", "Channel Thumbnail"),
                    ("topic_thumbnail", "Thumbnail"),
                    ("html5_zip", "HTML5 Zip"),
                    ("html5_dependency", "HTML5 Dependency (Zip format)"),
                    ("html5_thumbnail", "HTML5 Thumbnail"),
                    ("h5p", "H5P Zip"),
                    ("h5p_thumbnail", "H5P Thumbnail"),
                    ("slideshow_image", "Slideshow Image"),
                    ("slideshow_thumbnail", "Slideshow Thumbnail"),
                    ("slideshow_manifest", "Slideshow Manifest"),
                ],
                max_length=150,
            ),
        ),
        migrations.AlterField(
            model_name="localfile",
            name="extension",
            field=models.CharField(
                blank=True,
                choices=[
                    ("mp4", "MP4 Video"),
                    ("vtt", "VTT Subtitle"),
                    ("mp3", "MP3 Audio"),
                    ("pdf", "PDF Document"),
                    ("jpg", "JPG Image"),
                    ("jpeg", "JPEG Image"),
                    ("png", "PNG Image"),
                    ("gif", "GIF Image"),
                    ("json", "JSON"),
                    ("svg", "SVG Image"),
                    ("perseus", "Perseus Exercise"),
                    ("graphie", "Graphie Exercise"),
                    ("zip", "HTML5 Zip"),
                    ("h5p", "H5P"),
                    ("epub", "ePub Document"),
                ],
                max_length=40,
            ),
        ),
    ]
