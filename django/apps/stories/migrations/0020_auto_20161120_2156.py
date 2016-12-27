# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 20:56
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0019_auto_20160906_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, default='section-slug', editable=False, overwrite=True, populate_from=('title',), verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(allow_duplicates=True, blank=True, default='story-slug', editable=False, overwrite=True, populate_from=('title',), verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='storytype',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, default='storytype-slug', editable=False, overwrite=True, populate_from=('name',), verbose_name='slug'),
        ),
    ]