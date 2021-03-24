from django.http import HttpResponse
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
import requests

from .serializers import CartSerializer, OrderingSerializer, CartItemSerializer
from .models import Cart, CartItem
from .permissions import IsCartOwner


class ReorderAPI(GenericViewSet):
    """
    request Data format:
        [{id: X,  order: Y}, {id: X,  order: Y}, {id: X,  order: Y} ...]

    """

    @action(methods=('post',), detail=False)
    def reorder(self, request):

        serializer = OrderingSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        # if not serializer.is_valid():
        #     raise ValidationError(serializer.errors)
        # items = [
        #     self.queryset.model(
        #         id=item['id'], order=item['order']
        #     ) for order, item in enumerate(serializer.validated_data)
        # ]
        # self.queryset.model.objects.bulk_update(items, ['order'])
        return Response(status=status.HTTP_202_ACCEPTED)


class CartItemViewSets(ReorderAPI, ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [IsCartOwner]


class CartViewSets(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCartOwner]

    @action(detail=True, methods=['get'])
    def checkout(self, request, *args, **kwargs) -> HttpResponse:
        cart_object = self.get_object()
        serializer = self.serializer_class(cart_object)
        total_price = serializer.data.get('total_cost', 0)
        SLACK_WEBHOOK = None
        response = requests.post(url=SLACK_WEBHOOK, json={'text': f'Lasha Gogorishvili | Total Price - {total_price}'})
        if response.status_code == 200:
            return Response({'message': 'Successfully sent.!'}, status=status.HTTP_200_OK)

        return Response({'ERROR': f' Status Code: {response.status_code}, error :{response.text}'},
                        status=status.HTTP_400_BAD_REQUEST)
