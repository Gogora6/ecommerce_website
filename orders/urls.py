from rest_framework.routers import DefaultRouter

from .views import CouponViewSets, OrderViewSets

router = DefaultRouter()
router.register('coupons', CouponViewSets, basename='coupon')
router.register('orders', OrderViewSets, basename='order')
urlpatterns = router.urls
