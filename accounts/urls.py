from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, user_logout

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
]
