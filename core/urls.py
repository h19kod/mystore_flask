from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from products.views import home_view, product_detail_view, profile_view, register_view

urlpatterns = [
    # 1. لوحة تحكم المسؤول (Admin Panel)
    path('admin/', admin.site.urls),
    
    # 2. واجهات المتجر الرئيسية (Store Views)
    path('', home_view, name='home'),
    path('product/<slug:slug>/', product_detail_view, name='product-detail'),
    path('profile/', profile_view, name='profile'),
    
    # 3. نظام الحسابات (Authentication System)
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # 4. روابط الـ API والمنتجات الداخلية (Products App URLs)
    path('api/products/', include('products.urls')),
]

# 5. تفعيل عرض الصور المرفوعة (Media) والملفات الثابتة (Static) في بيئة التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)