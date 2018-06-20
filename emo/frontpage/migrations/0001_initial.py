# Generated by Django 2.0.4 on 2018-06-20 07:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='专属字符串')),
                ('occupy', models.BooleanField(verbose_name='是否使用中')),
            ],
        ),
    ]
