# Generated by Django 3.1.1 on 2020-09-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0007_auto_20200929_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalshippingcountryprice',
            name='state_province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='chemicalshippingcountryprice',
            name='state_province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coffeeshippingcountryprice',
            name='state_province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='materialshippingcountryprice',
            name='state_province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
