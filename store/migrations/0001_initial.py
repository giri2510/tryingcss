# Generated by Django 3.1 on 2020-08-29 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Finalorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Merchentdb',
            fields=[
                ('merch_id', models.IntegerField(primary_key=True, serialize=False)),
                ('merch_reggno', models.CharField(default='', max_length=500)),
                ('merch_shop', models.CharField(default='', max_length=500)),
                ('merch_address', models.CharField(default='', max_length=500)),
                ('merch_phone', models.CharField(default='', max_length=500)),
                ('merch_city', models.CharField(default='', max_length=500)),
                ('merch_state', models.CharField(default='', max_length=500)),
                ('merch_zip', models.CharField(default='', max_length=500)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('merch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Statuscheck',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('orderid', models.IntegerField(default='', null=True)),
                ('status', models.CharField(default='Order has been placed', max_length=5000)),
                ('ownerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('prod_id', models.IntegerField(primary_key=True, serialize=False)),
                ('prod_category', models.CharField(default='', max_length=500)),
                ('prod_subcategory', models.CharField(default='', max_length=500)),
                ('prod_name', models.CharField(default='', max_length=500, unique=True)),
                ('prod_desc', models.CharField(default='', max_length=5000)),
                ('prod_price', models.FloatField()),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='IMAGES/')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ownerprod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.merchentdb')),
            ],
        ),
        migrations.CreateModel(
            name='Orderitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('cust_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=500)),
                ('email', models.CharField(default='', max_length=500)),
                ('address', models.CharField(default='', max_length=500)),
                ('city', models.CharField(default='', max_length=500)),
                ('state', models.CharField(default='', max_length=500)),
                ('zip_code', models.CharField(default='', max_length=500)),
                ('phone', models.CharField(default='', max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('orderstatus', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('items', models.ManyToManyField(through='store.Finalorder', to='store.Orderitem')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='finalorder',
            name='orderitems',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orderitem'),
        ),
        migrations.AddField(
            model_name='finalorder',
            name='orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
        migrations.CreateModel(
            name='Orderupdate',
            fields=[
                ('update_id', models.IntegerField(primary_key=True, serialize=False)),
                ('orderid', models.IntegerField(default='', null=True)),
                ('finaldesc', models.CharField(blank=True, default='', max_length=500)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('update_desc', models.ManyToManyField(to='store.Statuscheck')),
            ],
            options={
                'unique_together': {('update_id', 'orderid')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='finalorder',
            unique_together={('orderitems', 'orders')},
        ),
    ]