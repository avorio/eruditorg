# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_office', '0002_add_i18n_and_backend_alias'),
        ('subscription', '0004_auto_20151005_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='renewalnotice',
            name='sent_emails',
            field=models.ManyToManyField(blank=True, verbose_name='Courriels envoyés', to='post_office.Email'),
        ),
    ]
