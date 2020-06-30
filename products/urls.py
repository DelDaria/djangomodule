from django.urls import path

from products import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='all_products'),
    path('create/', views.ProductCreate.as_view(), name='new_product'),
    path('edit/<int:pk>', views.ProductUpdate.as_view(), name='edit_product'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('<int:product_id>', views.product_by_id, name='product_by_id'),
    path('purchases/', views.PurchasesListView.as_view(), name='purchases'),
    path('refunds/', views.RefundsListView.as_view(), name='refunds'),

]