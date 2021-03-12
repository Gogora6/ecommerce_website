from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import requests

from .serializers import CartSerializer
from .models import Cart
from .permissions import IsCartOwner


class CartViewSets(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCartOwner]

    @action(detail=True, methods=['get'])
    def checkout(self, request, *args, **kwargs) -> HttpResponse:
        cart_object = self.get_object()
        serializer = self.serializer_class(cart_object)
        total_price = serializer.data.get('total_cost', 0)
        SLACK_WEBHOOK = 'https://hooks.slack.com/services/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'
        response = requests.post(url=SLACK_WEBHOOK, json={'text': f'Lasha Gogorishvili | Total Price - {total_price}'})
        if response.status_code == 200:
            return Response({'message': 'Successfully sent.!'}, status=status.HTTP_200_OK)

        return Response({'ERROR': f' Status Code: {response.status_code}, error :{response.text}'},
                        status=status.HTTP_400_BAD_REQUEST)
