from rest_framework import serializers
from .models import Product, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_info', 'product_categories_offered']

class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'category', 'description', 'supplier']
