# products/admin.py

from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)