from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
# تأكد من أن تطبيق orders موجود ولديه موديل Order، إذا لم يكن موجوداً احذف السطر بالأسفل
# from orders.models import Order 

# 1. الصفحة الرئيسية
def home_view(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    context = {
        'products': products, 
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'products/product_list.html', context)

# 2. صفحة تفاصيل المنتج
def product_detail_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        return render(request, 'products/product_detail.html', {'product': product})
    except Product.DoesNotExist:
        return redirect('home')

# 3. صفحة التسجيل (جديد)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'تم إنشاء الحساب بنجاح لـ {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 4. صفحة الملف الشخصي
@login_required
def profile_view(request):
    # إذا كان تطبيق orders غير مكتمل، اترك القائمة فارغة حالياً
    user_orders = [] 
    # user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': user_orders})

# --- API Classes ---
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer