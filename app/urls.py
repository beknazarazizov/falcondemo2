from django.contrib import admin
from django.urls import path, include
from app.views import ProductListView, ProductDetailTemplateView, AddProductView,DeleteProductView,EditProductView

urlpatterns = [
    path('index/',ProductListView.as_view(), name='index'),
    path('product-detail/<int:product_id>',ProductDetailTemplateView.as_view(), name='product_detail'),

    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('update_product/<int:pk>/',EditProductView.as_view(),name='update_product'),
    path('delete_product/<int:pk>/',DeleteProductView.as_view(), name='delete_product'),
]
