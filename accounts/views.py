from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import logout, login, authenticate
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from .serializers import UserRegisterSerializer, UserSerializer
from .models import User


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {}
        with transaction.atomic():
            user = serializer.save()
            token = Token.objects.create(user=user)
            data['Token'] = token.key
        return Response(data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """
    Check Email and password and return an AuthToken.
    """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {}
        user = User.objects.get(email=request.data.get('username'))
        token = Token.objects.get(user=user).key
        data['Token'] = token
        auth_user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if auth_user:
            request.session.set_expiry(86400)  # 1 day
            login(request, auth_user)
        return Response(data)


@api_view(http_method_names=['POST'])
def user_logout(request):
    logout(request)
    data = {'success': 'Successfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.auth
