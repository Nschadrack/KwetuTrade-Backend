# Generated by Django 3.1.1 on 2020-11-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0027_auto_20201108_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default-profile-pic.png', null=True, upload_to='customers/profiles'),
        ),
    ]
