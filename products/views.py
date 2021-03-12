from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from typing import Type

from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer, TagsSerializer, CreateProductSerializer
from .models import Category, Product, Tag

from cart.serializers import CartItemSerializer


class TagViewSets(ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class CategoryViewSets(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('order')
    lookup_field = 'slug'


class ProductViewSets(ModelViewSet):
    default_serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    filter_fields = ['category', 'price']
    search_fields = ['title']
    lookup_field = 'slug'

    serializer_by_action = {
        'create': CreateProductSerializer,
        'update': CreateProductSerializer,
    }

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.serializer_by_action.get(getattr(self, 'action', None), self.default_serializer_class)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, *args, **kwargs) -> HttpResponse:
        fields_data = {'fields': ['quantity']}
        serializer = CartItemSerializer(data=request.data, **fields_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            cart=self.request.user.cart,
            product=self.get_object()
        )

        return Response({'message': 'Product has been added to cart'}, status=status.HTTP_201_CREATED)
