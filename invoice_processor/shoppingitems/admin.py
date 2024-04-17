from django.contrib import admin
from .models import Brand, Product, Transaction

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Transaction)