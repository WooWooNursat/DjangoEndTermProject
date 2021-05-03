from django.contrib import admin
from main.models import Category, Product, Wear, Food, Cart, Order
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Wear)
admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(Order)