# Generated by Django 3.1 on 2020-08-29 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuscheck',
            name='orderid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]