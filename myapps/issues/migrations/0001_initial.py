# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrintIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('issue_name', models.CharField(max_length=50)),
                ('publication_date', models.DateField()),
                ('pages', models.IntegerField(editable=False, help_text='Number of pages')),
                ('pdf', models.FileField(null=True, upload_to='pdf/', blank=True, help_text='Pdf file for this issue.')),
                ('cover_page', sorl.thumbnail.fields.ImageField(null=True, upload_to='pdf/covers/', blank=True, help_text='An image file of the front page')),
                ('text', models.TextField(editable=False, help_text='Extracted from file.')),
            ],
            options={
                'ordering': ['-publication_date'],
                'verbose_name': 'Print issue',
                'verbose_name_plural': 'Print issues',
            },
            bases=(models.Model,),
        ),
    ]
