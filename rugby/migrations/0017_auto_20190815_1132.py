# Generated by Django 2.2.4 on 2019-08-15 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0016_auto_20190815_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='match',
            name='ratings_average',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rd',
        ),
        migrations.RemoveField(
            model_name='match',
            name='ref',
        ),
        migrations.RemoveField(
            model_name='match',
            name='stadium',
        ),
        migrations.RemoveField(
            model_name='match',
            name='tries_in_match',
        ),
        migrations.RemoveField(
            model_name='match',
            name='viewcount',
        ),
    ]
