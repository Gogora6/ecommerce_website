from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSets, CartItemViewSets

router = DefaultRouter()
router.register(r'cart', CartViewSets, basename='cart')
router.register(r'cart-item', CartItemViewSets, basename='cart-items')

urlpatterns = router.urls
