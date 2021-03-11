from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from .serializers import CategorySerializer, ProductSerializer, TagsSerializer, CreateProductSerializer
from .models import Category, Product, Tag


class TagViewSets(ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class CategoryViewSets(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('order')
    lookup_field = 'slug'


class ProductViewSets(ModelViewSet):
    default_serializer_class = ProductSerializer
    serializer_by_action = {
        'create': CreateProductSerializer,
        'update': CreateProductSerializer,
    }
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category', 'price']
    search_fields = ['title']
    lookup_field = 'slug'

    def get_serializer_class(self):
        return self.serializer_by_action.get(getattr(self, 'action', None), self.default_serializer_class)
