# Generated by Django 3.1.1 on 2020-11-06 06:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kwetuTrade', '0020_auto_20201028_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('advert_number', models.PositiveIntegerField(default=1, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('uploaded_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('advert_status', models.CharField(default='Deactive', max_length=30)),
                ('image', models.ImageField(upload_to='adverts/images')),
                ('caption', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderNotOnSiteItems',
            fields=[
                ('item_number', models.PositiveIntegerField(default=1, primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('image', models.ImageField(blank=True, null=True, upload_to='order_not_on_site/product_images')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='rejected_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='OrderNotOnSite',
            fields=[
                ('order_number', models.PositiveIntegerField(default=1, primary_key=True, serialize=False)),
                ('quantity_ordered', models.PositiveIntegerField()),
                ('amount_ordered', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ordered_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('out_of_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('delivered_date', models.DateTimeField(blank=True, null=True)),
                ('rejected_date', models.DateTimeField(blank=True, null=True)),
                ('order_status', models.CharField(default='pending', max_length=50)),
                ('newness_order_status', models.CharField(default='new', max_length=50)),
                ('email_address', models.EmailField(max_length=60)),
                ('phone_number', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_not_on_site', to='kwetuTrade.customer')),
                ('ordered_products', models.ManyToManyField(related_name='order_items', to='kwetuTrade.OrderNotOnSiteItems')),
            ],
        ),
    ]
