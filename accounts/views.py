from rest_framework import status, generics, permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout

from .models import User
from .permissions import IsUser
from .serializers import UserRegisterSerializer, UserSerializer


class RegistrationAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        data = {'token': token.key}
        return Response(data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """
    Check Email and password and return an AuthToken.
    """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.POST.get('username'))
        token = Token.objects.get(user=user).key
        data = {'token': token}
        return Response(data)


@api_view(http_method_names=['POST'])
def user_logout(request):
    logout(request)
    data = {'success': 'Successfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
