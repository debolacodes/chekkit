# Generated by Django 2.0.7 on 2018-09-08 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_auto_20180908_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=945506, null=True),
        ),
    ]
