# Generated by Django 3.1.1 on 2020-11-09 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0028_auto_20201109_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='customers/profiles/default-profile-pic.png', null=True, upload_to='customers/profiles'),
        ),
    ]