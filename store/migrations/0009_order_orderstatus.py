# Generated by Django 3.1 on 2020-09-03 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_order_orderstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderstatus',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
