from django.contrib import admin

from .models import Category, MenuItem, Cart, Order, OrderItem


admin.site.register(Category)
admin.site.register(MenuItem)
