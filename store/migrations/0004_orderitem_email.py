# Generated by Django 3.1 on 2020-08-31 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200829_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='email',
            field=models.CharField(default='', max_length=500),
        ),
    ]