from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # عرض معلومات شاملة في الجدول الرئيسي
    list_display = ['id', 'name', 'category', 'price', 'created_at']
    # إمكانية تعديل السعر مباشرة من الجدول بدون فتح صفحة المنتج
    list_editable = ['price'] 
    # إضافة فلاتر جانبية
    list_filter = ['category', 'created_at']
    # إضافة مربع بحث في الأعلى
    search_fields = ['name']
    # تقسيم الصفحة (كل 20 منتج بصفحة)
    list_per_page = 20
    prepopulated_fields = {'slug': ('name',)}