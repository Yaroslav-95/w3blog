# Generated by Django 2.0 on 2019-01-10 19:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0009_merge_20190104_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 10, 19, 1, 18, 209024), verbose_name='Publish date'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='weblog.Category', verbose_name='Parent category'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
