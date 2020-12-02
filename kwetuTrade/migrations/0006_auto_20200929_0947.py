# Generated by Django 3.1.1 on 2020-09-29 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0005_auto_20200928_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='animal_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='chemical_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='coffee_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coffeeweight',
            name='unit_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='material',
            name='material_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shippingcountryprice',
            name='shippingcountryprice_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shippingfee',
            name='shippingfee_ID',
            field=models.PositiveIntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
