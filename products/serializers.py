from rest_framework import serializers

from .models import Category, Product, Tag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'brand',
            'category',
            'description',
            'ingredients',
            'UPC',
            'SKU',
            'image',
            'price',
            'stocks'
        )
