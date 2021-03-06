# Generated by Django 2.2.7 on 2019-11-21 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0003_auto_20191118_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.TimeField(auto_now_add=True)),
                ('phone_number', models.CharField(db_index=True, max_length=15)),
                ('client_id', models.CharField(db_index=True, max_length=10)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='OrderRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail.Item')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail.Order')),
            ],
        ),
    ]
