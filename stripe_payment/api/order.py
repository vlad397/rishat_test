import requests

from stripe_payment.settings import ORDER_SESSION_ID

USD = 60.50
RUB = 0.017


class Order(object):
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(ORDER_SESSION_ID)
        if not cart:
            cart = self.session[ORDER_SESSION_ID] = {}
        self.cart = cart

    def add(self, item):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        if item.name not in self.cart:
            self.cart[item.name] = {'quantity': 1, 'price': item.price, 'curr': item.currency}
        else:
            self.cart[item.name]['quantity'] += 1
            self.cart[item.name]['price'] += item.price
        self.session.modified = True

    def remove(self, item):
        """
        Удаление товара из корзины.
        """
        if item.name in self.cart:
            if self.cart[item.name]['quantity'] > 1:
                self.cart[item.name]['quantity'] -= 1
                self.cart[item.name]['price'] -= item.price
            else:
                del self.cart[item.name]
            self.session.modified = True
            return True
        return False

    def convert_currency(self, curr_from, curr_to, amount):
        """
        Конвертация валют
        """
        url = f'http://open.er-api.com/v6/latest/{curr_from}'
        data = requests.get(url).json()
        if data['result'] == 'success':
            exchange_rate = data['rates']
            return exchange_rate[curr_to.upper()] * amount
        exchange_rate = USD if curr_from == 'usd' else RUB
        return exchange_rate * amount

    def get_total_price(self, currency):
        """
        Подсчет стоимости товаров в корзине.
        """
        if self.cart == {}:
            return False
        items_currs = {}
        for _, data in self.cart.items():
            if data['curr'] == 'rub':
                items_currs['rub'] = data['price']
            else:
                items_currs['usd'] = data['price']
        currency_from = 'rub' if currency == 'usd' else 'usd'
        pre_result = self.convert_currency(currency_from, currency, items_currs[currency_from])
        result = items_currs[currency] + pre_result
        return result

    def clear(self):
        """
        Очистка корзины
        """
        if self.session[ORDER_SESSION_ID] == {}:
            return False
        del self.session[ORDER_SESSION_ID]
        self.session.modified = True
        return True
