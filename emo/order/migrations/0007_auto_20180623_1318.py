# Generated by Django 2.0.4 on 2018-06-23 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_dishrecord_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishrecord',
            name='name',
            field=models.CharField(max_length=150, verbose_name='菜名'),
        ),
    ]
