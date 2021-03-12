from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSets

router = DefaultRouter()
router.register(r'cart', CartViewSets, basename='category')

urlpatterns = router.urls
