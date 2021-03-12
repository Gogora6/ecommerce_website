from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import Coupon, Order


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = (
            'code',
            'expiration_date',
            'discount'
        )


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'products',
            'coupon',
            'user',
            'price',
            'created_date',
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = (
            'id',
            'products',
            'coupon',
            'user',
            'price',
            'created_date',
        )
