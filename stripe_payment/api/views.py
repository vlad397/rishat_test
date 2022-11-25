from http import HTTPStatus
from math import ceil

import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from stripe_payment.settings import (CANCEL_LINK, STRIPE_PUBLISHABLE_KEY,
                                     STRIPE_SECRET_KEY, SUCCESS_LINK)

from .models import Discount, Item
from .order import Order
from .serializers import ItemSerializer

stripe.api_key = STRIPE_SECRET_KEY


id_param = [
    openapi.Parameter(
        "id",
        openapi.IN_PATH,
        description="ID предмета",
        type=openapi.TYPE_INTEGER
    )
]

currency_param = [
    openapi.Parameter(
        "currency",
        openapi.IN_PATH,
        description="Валюта, в которую автоматически будут конвертированы "
                    "цены всех товаров(округление в большую сторону)",
        type=openapi.TYPE_STRING,
        enum=['usd', 'rub']
    )
]


class ItemGetView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item.html'

    @swagger_auto_schema(operation_description="HTML страница с информацией о покупке и кнопкой 'Buy'"
                                               ", перенаправляющей на скрытый метод api/buy/{id}",
                         manual_parameters=id_param)
    def get(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        serializer = ItemSerializer(item)
        return Response({'serializer': serializer, 'item': item, 'stripe_pub_key': STRIPE_PUBLISHABLE_KEY},
                        status=HTTPStatus.OK)


class ItemBuyView(APIView):
    swagger_schema = None

    def get(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=SUCCESS_LINK,
            cancel_url=CANCEL_LINK,
        )

        return Response(session.id, status=HTTPStatus.OK)


@swagger_auto_schema(method='get', auto_schema=None)
@api_view(['GET'])
def success(request):
    return HttpResponse('Оплачено!')


@swagger_auto_schema(method='get', auto_schema=None)
@api_view(['GET'])
def cancel(request):
    return HttpResponse('Оплата не прошла!')


class OrderDetailView(APIView):
    @swagger_auto_schema(operation_description="Добавление товара в корзину",
                         manual_parameters=id_param)
    def post(self, request, pk):
        order = Order(request)
        item = get_object_or_404(Item, id=pk)
        order.add(item)
        return Response('Добавлено в корзину', status=HTTPStatus.CREATED)

    @swagger_auto_schema(operation_description="Удаление товара из корзины",
                         manual_parameters=id_param)
    def delete(self, request, pk):
        order = Order(request)
        item = get_object_or_404(Item, id=pk)
        result = order.remove(item)
        if result:
            return Response('Удалено из корзины', status=HTTPStatus.OK)
        return Response('Данного товара нет в корзине', status=HTTPStatus.NOT_FOUND)


class OrderView(APIView):
    @swagger_auto_schema(operation_description="Просмотр содержимого корзины")
    def get(self, request):
        order = Order(request)
        cart = order.cart
        return Response(cart)

    @swagger_auto_schema(operation_description="Очистка корзины")
    def delete(self, request):
        order = Order(request)
        result = order.clear()
        if result:
            return Response('Корзина очищена', status=HTTPStatus.OK)
        return Response('Корзина уже пуста', status=HTTPStatus.NOT_FOUND)


class OrderGetView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order.html'

    @swagger_auto_schema(operation_description="HTML страница с информацией о выбранных товарах и кнопкой 'Buy'"
                                               ", перенаправляющей на скрытый метод api/order_buy/{currency}",
                         manual_parameters=currency_param)
    def get(self, request, currency):
        if currency not in ['usd', 'rub']:
            return HttpResponse('Возможные варианты: usd, rub')
        order = Order(request)
        cart = order.cart
        result = ceil(order.get_total_price(currency))
        if not result:
            return HttpResponse('Сначала нужно добавить товары в корзину!')
        return Response({'cart': cart, 'result': result, 'currency': currency,
                        'stripe_pub_key': STRIPE_PUBLISHABLE_KEY})


class OrderBuyView(APIView):
    swagger_schema = None

    def get(self, request, currency):
        order = Order(request)
        cart = order.cart
        unit_amount = ceil(order.get_total_price(currency))
        discount = Discount.objects.filter().last()
        if discount:
            discount_curr = discount.stripe_coupon_id_usd if currency == 'usd' else discount.stripe_coupon_id_rub
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': currency,
                    "tax_behavior": "exclusive",
                    'product_data': {
                        'name': ', '.join(cart.keys()),
                    },
                    'unit_amount': unit_amount * 100,
                },
                'quantity': 1,
            }],
            automatic_tax={'enabled': True, },
            mode='payment',
            discounts=[{'coupon': discount_curr, }] if discount else [],
            success_url=SUCCESS_LINK,
            cancel_url=CANCEL_LINK,
        )

        return Response(session.id, status=HTTPStatus.OK)
