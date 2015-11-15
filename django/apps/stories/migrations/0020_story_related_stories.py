# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0019_auto_20151115_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='related_stories',
            field=models.ManyToManyField(to='stories.Story', verbose_name='related stories'),
        ),
    ]
