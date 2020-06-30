from django.forms import ModelForm

from products import models


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        exclude = ['picture']
