# Generated by Django 2.0.7 on 2018-09-08 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20180806_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=821898, null=True),
        ),
    ]
