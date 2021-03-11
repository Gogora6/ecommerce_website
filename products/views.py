from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import CategorySerializer, ProductSerializer, TagsSerializer
from .models import Category, Product, Tag


class CategoryViewSets(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        category = self.get_serializer(queryset, many=True)
        tags = TagsSerializer(Tag.objects.all(), many=True)

        data = {
            'category': category.data,
            'tags': tags.data
        }
        return Response(data)


class ProductViewSets(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
