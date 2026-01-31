from django.urls import path
from .views import (
    ProductList, ProductDetail, CategoryList, 
    home_view, product_detail_view
)

urlpatterns = [
    # روابط الـ API
    path('api/', ProductList.as_view(), name='product-list-api'),
    path('api/<int:id>/', ProductDetail.as_view(), name='product-detail-api'),
    path('api/categories/', CategoryList.as_view(), name='category-list-api'),
    
    # روابط الصفحات الرسومية
    path('', home_view, name='home'),
    path('product/<slug:slug>/', product_detail_view, name='product-detail'),
]