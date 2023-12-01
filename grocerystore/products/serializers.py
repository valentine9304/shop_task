# products/serializers.py
from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Category, SubCategory, Product, ShoppingCart


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            "name",
            "slug",
            "image",
        ]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["name", "slug", "image", "subcategories"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "subcategory",
            "price",
            "image",
            "image2",
            "image3",
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)
    product = ProductSerializer(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    sum = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("user", "product", "price", "quantity", "sum")

    def get_price(self, obj):
        return obj.product.price if obj.product else None

    def get_sum(self, obj):
        return obj.quantity * obj.product.price
