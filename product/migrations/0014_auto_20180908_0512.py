# Generated by Django 2.0.7 on 2018-09-08 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20180908_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=802956, null=True),
        ),
    ]
