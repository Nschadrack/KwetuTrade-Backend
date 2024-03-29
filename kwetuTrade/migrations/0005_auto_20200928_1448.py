# Generated by Django 3.1.1 on 2020-09-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0004_auto_20200928_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images'),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images'),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images'),
        ),
        migrations.AlterField(
            model_name='material',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images'),
        ),
    ]
