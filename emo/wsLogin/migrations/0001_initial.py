# Generated by Django 2.0 on 2018-06-23 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WxUser',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('session_id', models.CharField(max_length=150, verbose_name='session_id')),
                ('nickname', models.CharField(max_length=150, verbose_name='昵称')),
                ('sex', models.IntegerField(verbose_name='性别')),
                ('province', models.CharField(max_length=150, verbose_name='省份')),
                ('city', models.CharField(max_length=150, verbose_name='城市')),
                ('country', models.CharField(max_length=150, verbose_name='城市')),
                ('headimgurl', models.CharField(max_length=150, verbose_name='头像')),
                ('privilege', models.CharField(max_length=150, verbose_name='特权')),
                ('unionid', models.CharField(max_length=150, verbose_name='统一标识')),
            ],
        ),
    ]
