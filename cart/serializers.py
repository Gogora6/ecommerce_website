from django.db.models import Sum, F
from rest_framework import serializers

from .models import CartItem, Cart
from django.db import models
from products.serializers import ProductSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
        A ModelSerializer that takes an additional `fields` argument that
        controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        selection_fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if selection_fields:
            allowed_fields = set(selection_fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed_fields:
                self.fields.pop(field_name)


class CartItemSerializer(DynamicFieldsModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'active', 'cart')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_cost = serializers.SerializerMethodField(method_name='get_total_cost')

    class Meta:
        model = Cart
        fields = ('id', 'total_cost', 'items')

    @staticmethod
    def get_total_cost(obj):
        return CartItem.objects.filter(cart_id=obj.id, active=True).aggregate(
            cost=Sum(F('quantity') * F('product__price'), output_field=models.CharField()))['cost']
