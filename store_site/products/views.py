from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from products import models as product_models
from products import forms
from users import models as user_models


# Create your views here.


def index(request):
    return render(request, 'home_page.html')


class ProductsListView(ListView):
    model = product_models.Product
    queryset = product_models.Product.objects.all()
    ordering = 'name'

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id', '')
        amount = int(request.POST.get('amount', ''))
        user_id = int(request.POST.get('user_id', ''))
        user = user_models.User.objects.get(pk=user_id)
        product = product_models.Product.objects.get(pk=product_id)

        product.amount -= amount
        user.cash -= amount * product.price
        if product.amount < 0 or user.cash < 0:
            return render(request, 'products/warning.html', {'product': product, 'user': user})
        else:
            purchase = product_models.Purchase(user=user, product=product, amount=amount)
            user.save()
            product.save()
            purchase.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProductCreate(CreateView):
    model = product_models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('all_products')


class ProductUpdate(UpdateView):
    model = product_models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('all_products')


class ProductDetailView(DetailView):
    model = product_models.Product
    context_object_name = 'product'


def product_by_id(request, product_id):
    try:
        product = product_models.Product.objects.get(id=product_id)
    except (product_models.Product.DoesNotExist, product_models.Product.MultipleObjectsReturned):
        return redirect('/')
    return render(request, 'products/product_by_id.html', {'product': product})


class PurchasesListView(ListView):
    template_name = 'products/purchases_list.html'
    model = product_models.Purchase
    ordering = 'created_at'

    def get_queryset(self):
        return product_models.Purchase.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        purchase_id = request.POST.get('purchase_id', '')
        purchase = product_models.Purchase.objects.get(pk=purchase_id)
        refund = product_models.Refund.objects.filter(purchase=purchase)
        a = len(refund)
        if a == 0:
            refund = product_models.Refund(purchase=purchase)
            refund.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'products/refund_warning.html')


class RefundsListView(ListView):
    template_name = 'products/refund_admin_list.html'
    model = product_models.Refund
    queryset = product_models.Refund.objects.filter(admin_confirmed=None)
    ordering = 'created_at'

    # def get_queryset(self):
    #     a = product_models.Refund.objects.all()
    #     for i in a:
    #         pass
    #     return a

    def post(self, request, *args, **kwargs):
        refund_id = request.POST.get('refund_id', '')
        refund = product_models.Refund.objects.get(pk=refund_id)
        if 'decline' in request.POST:
            refund.admin_confirmed = False
        elif 'approve' in request.POST:
            refund.admin_confirmed = True
            # user = user_models.User.objects.get(pk=refund.purchase.user.pk)
            refund.purchase.user.cash += refund.purchase.amount*refund.purchase.product.price
            refund.purchase.user.save()
            # product = user_models.User.objects.get(pk=refund.purchase.user.pk)
            refund.purchase.product.amount += refund.purchase.amount
            refund.purchase.product.save()
        refund.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))