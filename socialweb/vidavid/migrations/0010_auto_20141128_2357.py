# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vidavid', '0009_auto_20141128_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='tag',
            name='posts',
            field=models.ManyToManyField(to='vidavid.Post'),
            preserve_default=True,
        ),
    ]
