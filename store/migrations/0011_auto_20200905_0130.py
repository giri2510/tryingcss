# Generated by Django 3.1 on 2020-09-04 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_orderitem_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statuscheck',
            name='ownerid',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='Orderupdate',
        ),
        migrations.DeleteModel(
            name='Statuscheck',
        ),
    ]