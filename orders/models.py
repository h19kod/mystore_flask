from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    # خيارات حالة الطلب
    STATUS_CHOICES = (
        ('Pending', 'قيد الانتظار'),
        ('Shipped', 'تم الشحن'),
        ('Delivered', 'تم التوصيل'),
        ('Cancelled', 'تم الإلغاء'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    # إضافة حالة الطلب هنا
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"