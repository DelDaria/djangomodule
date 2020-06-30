from django.contrib import admin
from . import models

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'amount']
    list_editable = ['name', 'amount', 'price']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Purchase)
admin.site.register(models.Refund)

