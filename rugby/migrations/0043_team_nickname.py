# Generated by Django 2.2.5 on 2020-08-13 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0042_auto_20200721_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='nickname',
            field=models.TextField(default=''),
        ),
    ]