# Generated by Django 2.2.4 on 2019-12-14 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0035_auto_20191213_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='try',
            name='error',
            field=models.IntegerField(default=0),
        ),
    ]
