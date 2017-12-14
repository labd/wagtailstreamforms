# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 22:38
from __future__ import unicode_literals

from django.db import migrations
import wagtailstreamforms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailstreamforms', '0005_baseform_error_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailform',
            name='to_addresses',
            field=wagtailstreamforms.fields.MultiEmailField(help_text='Add one email per line'),
        ),
    ]
