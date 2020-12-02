# Generated by Django 3.1.1 on 2020-11-07 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0022_auto_20201106_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderNotOnSiteItem',
            fields=[
                ('item_number', models.PositiveIntegerField(default=1, primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('image', models.ImageField(blank=True, null=True, upload_to='order_not_on_site/product_images')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='OrderNotOnSiteItems',
        ),
        migrations.AlterField(
            model_name='ordernotonsite',
            name='ordered_products',
            field=models.ManyToManyField(related_name='order_items', to='kwetuTrade.OrderNotOnSiteItem'),
        ),
    ]
