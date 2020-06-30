from django.contrib import admin
from . import models
from products import models as prod_models

# Register your models here.


class ProductsInline(admin.TabularInline):
    model = prod_models.Purchase
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ProductsInline]
    list_display = ['username']


admin.site.register(models.User, UserAdmin)
