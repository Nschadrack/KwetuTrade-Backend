# Generated by Django 3.1.1 on 2020-09-27 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0002_auto_20200927_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='status',
            field=models.CharField(default='Deactive', max_length=30),
        ),
    ]
