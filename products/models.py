from django.db import models

# 1. جدول التصنيفات
class Category(models.Model):
    name = models.CharField(max_length=255)
    # slug هو الاسم الذي يظهر في الرابط (مثل: /category/mobile-phones)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories' # لتصحيح الاسم في لوحة التحكم

    def __str__(self):
        return self.name

# 2. جدول المنتجات
class Product(models.Model):
    # التصحيح هنا: استخدمنا on_delete بدلاً من on_middleware
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # سعر دقيق (مثل 99.99)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # تاريخ الإضافة تلقائياً

    def __str__(self):
        return self.name