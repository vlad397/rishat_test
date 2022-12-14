# РИШАТ - тестовое задание

### Задание
См. [issue](https://github.com/vlad397/rishat_test/issues/1)

### Развернутый проект для тестирования
Проект доступен по адресу *http://158.160.3.136*

`Swagger` документация доступна по адресу *http://158.160.3.136/swagger/*

`Redoc` документация доступна по адресу *http://158.160.3.136/redoc/*

`Админка` доступна по адресу *http://158.160.3.136/admin/*

`Данные админки` - admin admin

`Все остальные методы` доступны по адресу *http://158.160.3.136/api/...*

Проект развернут в Yandex Cloud 25.11.2022 в 18:00 мск специально для просмотра тестового задания.
Будет доступен ограниченное кол-во времени из-за пробного периода.

### Описание

`Swagger` документация доступна по адресу *http://127.0.0.1/swagger/*

`Redoc` документация доступна по адресу *http://127.0.0.1/redoc/*

`Админка` доступна по адресу *http://127.0.0.1/admin/*


Из документации исключены страницы `/buy/{id}` и `/order_buy/{currency}`, т.к. это страницы, вызываемые методами 
`/item/{id}` и `/order_preview/{currency}` соответствено и возвращающие *Stripe session id*.


Возможности проекта:

- админ: создание товара, создание скидки;
- покупка одного товара через платформу Stripe;
- добавление товаров в корзину (на основе сессий);
- удаление товаров из корзины;
- очистка корзины;
- покупка всех товаров из корзины с выбором валюты оплаты и автоматической конвертацией через ExchangeRate-API.
Округление происходит в большую сторону. При оформлении покупки отображается скидка и налог. Скидка берется
последняя созданная, просто как тест для правильного отображения. Налог меняется в зависимости от выбранной страны.


### Подробности выполнения

Модели: `Item`, `Discount`.
Поля модели `Item`:
- name;
- description;
- price;
- currency - весь проект реализовано в соответствии с 2 возможными валютами: usd и rub.

Поля модели `Discount`:
- name;
- description;
- percent_of - процент скидки
- stripe_coupon_id_usd - id Stripe купона для usd (по умолчанию null);
- stripe_coupon_id_rub - id Stripe купона для rub (по умолчанию null).


При создании объекта модели `Discount` на панели администратора сработает `post_save()` сигнал, который создаст
`stripe.Coupon` объект в двух валютах и обновит соответствующие поля модели `Discount`. Скидка и налог прикручиваются
только к корзине, т.е. для покупки единичных товаров скидки и налога нет.


### Запуск проекта
После клонирования репозитария создайте `.env` файл на уровне с `env_sample.txt` - шаблоном env-файла

Для установки Docker используйте команду `sudo apt install docker docker-compose`

Далее выполните следующие команды:

`sudo docker-compose up -d --build` *Для запуска сборки контейнеров*

`sudo docker-compose exec backend python manage.py makemigrations` *Для создания миграций*

`sudo docker-compose exec backend python manage.py migrate` *Для применения миграций*

`sudo docker-compose exec backend python manage.py createsuperuser` *Для создания суперпользователя*

`sudo docker-compose exec backend python manage.py collectstatic` *Для сбора статических файлов*

Далее зайдите в панель администратора и создайте объекты моделей `Item` и `Discount`.
