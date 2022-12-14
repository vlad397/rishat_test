# Generated by Django 3.2 on 2022-11-23 09:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20221123_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='percent_of',
            field=models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)], verbose_name='Процент скидки'),
            preserve_default=False,
        ),
    ]
