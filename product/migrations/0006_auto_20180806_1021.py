# Generated by Django 2.0.7 on 2018-08-06 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20180806_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=141953, null=True),
        ),
    ]
