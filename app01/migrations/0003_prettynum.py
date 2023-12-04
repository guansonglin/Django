# Generated by Django 3.2.16 on 2023-04-25 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20230422_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32, verbose_name='手机号')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(1, '1级'), (2, '2级'), (3, '3级'), (4, '4级')], default=1, verbose_name='级别')),
                ('status', models.SmallIntegerField(choices=[(1, '未购买'), (2, '已购买')], default=1, verbose_name='状态')),
            ],
        ),
    ]
