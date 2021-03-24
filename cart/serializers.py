from rest_framework import serializers

from .models import CartItem, Cart


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
    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'active')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_cost')


class OrderingSerializer(serializers.Serializer):
    pk = serializers.ListSerializer()
    pk = serializers.IntegerField(validators=[])

