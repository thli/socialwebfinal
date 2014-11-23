# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vidavid', '0005_auto_20141122_1850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='profile',
            new_name='user',
        ),
    ]
