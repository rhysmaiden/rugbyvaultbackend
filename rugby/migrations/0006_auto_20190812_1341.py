# Generated by Django 2.2.4 on 2019-08-12 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0005_auto_20190812_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='try',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rugby.Team'),
        ),
    ]