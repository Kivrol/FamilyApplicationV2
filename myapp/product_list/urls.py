from django.urls import path
from . import views

urlpatterns = [
        path('', views.ProductList.as_view(), name='product_list'),
        path('delete/<int:id>', views.DeleteProduct.as_view(), name='delete_product'),
]