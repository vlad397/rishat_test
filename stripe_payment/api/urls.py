from django.urls import path

from .views import (ItemBuyView, ItemGetView, OrderBuyView, OrderDetailView,
                    OrderGetView, OrderView, cancel, success)

urlpatterns = [
    path('item/<int:pk>', ItemGetView.as_view(), name='item_get'),
    path('buy/<int:pk>', ItemBuyView.as_view(), name='item_buy'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order_preview/<str:currency>', OrderGetView.as_view(), name='order_preview'),
    path('order_buy/<str:currency>', OrderBuyView.as_view(), name='order_buy'),
    path('success/', success),
    path('cancel/', cancel)
]
