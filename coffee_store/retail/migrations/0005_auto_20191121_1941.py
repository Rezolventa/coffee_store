# Generated by Django 2.2.7 on 2019-11-21 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0004_auto_20191121_1911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderrow',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='orderrow',
            old_name='order_id',
            new_name='order',
        ),
    ]
