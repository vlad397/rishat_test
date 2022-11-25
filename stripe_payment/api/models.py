import stripe
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

CURRENCIES = [
    ('usd', 'USD'),
    ('rub', 'RUB'),
]


class Item(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Название товара'
    )
    description = models.TextField(
        verbose_name='Описание товара'
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена товара'
    )
    currency = models.CharField(
        choices=CURRENCIES, max_length=10, verbose_name='Валюта товара'
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return f'{self.name}(id={self.id})'


class Discount(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Название скидки', unique=True
    )
    description = models.TextField(
        verbose_name='Описание скидки'
    )
    percent_of = models.PositiveSmallIntegerField(
        verbose_name='Процент скидки', validators=[MaxValueValidator(99), MinValueValidator(1)]
    )
    stripe_coupon_id_usd = models.CharField(
        max_length=150, verbose_name='Stripe id скидки для usd', unique=True, blank=True, null=True
    )
    stripe_coupon_id_rub = models.CharField(
        max_length=150, verbose_name='Stripe id скидки для rub', unique=True, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name


@receiver(post_save, sender=Discount)
def create_profile(sender: Discount, instance: Discount, created: bool, **kwargs) -> bool:
    if created:
        coupon_usd = stripe.Coupon.create(percent_off=instance.percent_of, duration="once", currency='usd')
        coupon_rub = stripe.Coupon.create(percent_off=instance.percent_of, duration="once", currency='rub')
        instance.stripe_coupon_id_usd = coupon_usd.id
        instance.stripe_coupon_id_rub = coupon_rub.id
        instance.save()
        return True
    return False
