# Generated by Django 2.0.7 on 2018-09-08 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20180908_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=454229, null=True),
        ),
    ]
