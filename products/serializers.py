from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    # لجعل اسم التصنيف يظهر بدلاً من الرقم
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 
            'slug', 'description', 'price', 'image', 'created_at'
        ]