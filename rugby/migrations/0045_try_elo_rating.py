# Generated by Django 3.1 on 2020-08-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0044_match_region_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='try',
            name='elo_rating',
            field=models.IntegerField(default=1000),
        ),
    ]