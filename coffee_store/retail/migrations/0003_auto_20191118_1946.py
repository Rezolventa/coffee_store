# Generated by Django 2.2.7 on 2019-11-18 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0002_auto_20191114_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]