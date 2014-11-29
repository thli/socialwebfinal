# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vidavid', '0011_auto_20141129_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(default='hi', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default='hi', max_length=20),
            preserve_default=False,
        ),
    ]
