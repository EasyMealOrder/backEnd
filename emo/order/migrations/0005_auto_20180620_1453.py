# Generated by Django 2.0.4 on 2018-06-20 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_dishrecord_finished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishrecord',
            name='orderID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
    ]
