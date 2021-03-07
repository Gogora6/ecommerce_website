from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product


class CategoryViewSets(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewSets(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
