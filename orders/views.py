from django.db.models import Sum
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import CouponSerializer, OrderSerializer, OrderCreateSerializer
from .models import Coupon, Order
from products.models import Product


class CouponViewSets(ModelViewSet):
    serializer_class = CouponSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all()


class OrderViewSets(ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    default_serializer_class = OrderSerializer

    serializer_by_action = {
        'create': OrderCreateSerializer,
        'update': OrderCreateSerializer
    }

    def perform_create(self, serializer):
        products_ids = self.request.data.getlist('products')
        products_prices = Product.objects.filter(pk__in=products_ids)
        sum_price = products_prices.aggregate(Sum('price')).get('price__sum')
        if self.request.data.get('coupon'):
            # @TODO ADD COUPON NAME
            coupon: Coupon = Coupon.objects.filter(id=self.request.data.get('coupon'))
            sum_price = sum_price * coupon.discount / 100
        serializer.save(user=self.request.user, price=sum_price)

    def get_serializer_class(self):
        return self.serializer_by_action.get(getattr(self, 'action', None), self.default_serializer_class)
