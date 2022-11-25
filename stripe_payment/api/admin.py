from django.contrib import admin

from .models import Discount, Item

admin.site.register(Item)
admin.site.register(Discount)
