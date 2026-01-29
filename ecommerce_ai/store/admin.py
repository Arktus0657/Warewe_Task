from django.contrib import admin

# Register your models here.
from .models import Product, CartItem, Order, UserInteraction

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(UserInteraction)
