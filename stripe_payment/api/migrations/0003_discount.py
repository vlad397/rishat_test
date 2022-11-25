# Generated by Django 3.2 on 2022-11-23 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20221122_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название скидки')),
                ('description', models.TextField(verbose_name='Описание скидки')),
                ('stripe_coupon_id_usd', models.CharField(max_length=150, null=True, unique=True, verbose_name='Stripe id скидки для usd')),
                ('stripe_coupon_id_rub', models.CharField(max_length=150, null=True, unique=True, verbose_name='Stripe id скидки для rub')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
            },
        ),
    ]
