from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from products.models import Product

@api_view(['POST'])
@permission_classes([AllowAny]) # خليناها AllowAny مؤقتاً لسهولة الفحص بدون توكن
def create_order(request):
    """
    هذه الدالة تستقبل قائمة المنتجات وتحولها إلى طلب حقيقي في قاعدة البيانات
    """
    data = request.data
    order_items = data.get('order_items')

    # التأكد من أن السلة ليست فارغة
    if not order_items or len(order_items) == 0:
        return Response(
            {'detail': 'فشل الطلب: السلة فارغة، يرجى إضافة منتجات'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # مؤقتاً نربط الطلب بأول مستخدم موجود (الآدمن) لغرض التجربة
        from django.contrib.auth.models import User
        user = User.objects.get(id=1)

        # 1. إنشاء رأس الطلب (Order Header)
        order = Order.objects.create(
            user=user, 
            total_price=0,
            status='Pending'
        )

        total_sum = 0

        # 2. إضافة المنتجات (Order Items) وحساب السعر
        for item in order_items:
            product = Product.objects.get(id=item['product'])
            
            # إنشاء عنصر الطلب
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
                price=product.price # نأخذ السعر الحالي للمنتج
            )
            
            # إضافة سعر هذا العنصر للمجموع الكلي
            total_sum += product.price * order_item.quantity

        # 3. تحديث السعر الإجمالي النهائي للطلب
        order.total_price = total_sum
        order.save()

        return Response({
            'detail': 'تم إنشاء الطلب بنجاح وهو الآن قيد الانتظار',
            'order_id': order.id,
            'total_price': total_sum
        }, status=status.HTTP_201_CREATED)

    except Product.DoesNotExist:
        return Response(
            {'detail': 'أحد المنتجات غير موجود في المتجر'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'detail': f'حدث خطأ غير متوقع: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )